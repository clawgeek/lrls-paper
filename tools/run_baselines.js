// Baseline comparison for LRLS: identical objective field, identical
// constraint gate, identical evaluation budget.
//
// Methods
//   LRLS   - the specification's two-pool + scheduler solver (from solver_core.js)
//   RS     - random search over the domain
//   SA     - simulated annealing with a fixed geometric cooling schedule
//   COA-T  - temperature-gated two-phase switch (explore above T*, exploit below),
//            the mechanism the paper argues against
//   SP-EA  - single population, entropy coefficient annealed, no role separation
//
// Budget: every method receives the same number of fval() evaluations as the
// LRLS run of that (profile, seed), so the comparison is budget-matched.
//
// Metrics: best feasible value (risk < 0.35 gate), evaluation index of the first
// feasible sample, violation count (samples landing in hazard zones), coverage.
//
// Usage: node run_baselines.js > baseline_data.json
const fs = require('fs');
const path = require('path');

const coreSrc = fs.readFileSync(path.join(__dirname, 'solver_core.js'), 'utf8');
const FEAS = 0.35; // feasibility gate: risk(x,z) < 0.35, same as globalMax()

// --- instrument the core: count evaluations, track first/best feasible ---
let src = coreSrc
  .replace('function fval(F,x,z){', 'function fval(F,x,z){EV.n++;')
  .replace(
    'return clamp(v,0,1);',
    'const _c=clamp(v,0,1);const _risk=risk(F,x,z);' +
    'if(_risk<' + FEAS + '){if(_c>EV.best){EV.best=_c;}if(EV.first<0)EV.first=EV.n;' +
    'if(EV.n95<0&&_c>=globalThis.THR95)EV.n95=EV.n;' +
    'if(EV.n99<0&&_c>=globalThis.THR99){EV.n99=EV.n;EV.vioAt99=EV.vio;}}else{EV.vio++;}' +
    'return clamp(v,0,1);'
  )
  .replace('mulberry32(20261105)', 'mulberry32(globalThis.SEED)');

const api = new Function(src + '\nreturn {simulate,makeField,fval,risk,CFG};')();
const { simulate, makeField, fval, risk, CFG } = api;

const EV = { n: 0, best: 0, bestN: 0, first: -1, vio: 0, n95: -1, n99: -1, vioAt99: 0 };
globalThis.EV = EV;

const PROFILES = [
  { name: 'P1-mild', params: { lambdaE: .35, risk: .25, complexity: .20, stress: 0 } },
  { name: 'P2-baseline', params: { lambdaE: .35, risk: .55, complexity: .50, stress: 0 } },
  { name: 'P3-highrisk', params: { lambdaE: .30, risk: .68, complexity: .62, stress: .30 } },
  { name: 'P4-extreme', params: { lambdaE: .15, risk: .90, complexity: .85, stress: .90 } },
];
const SEEDS = [1, 2, 3, 4, 5];

function resetEV() { EV.n = 0; EV.best = 0; EV.bestN = 0; EV.first = -1; EV.vio = 0; EV.n95 = -1; EV.n99 = -1; EV.vioAt99 = 0; }

// box-constrained domain used by the terrain
const H = CFG.HALF;
const clampv = (v, a, b) => (v < a ? a : v > b ? b : v);

function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function gauss(rnd, s) {
  // Box-Muller
  const u = Math.max(rnd(), 1e-9), v = rnd();
  return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v) * s;
}

// budget-matched evaluation that feeds the shared metrics
function evaluate(F, x, z) {
  const v = fval(F, x, z);
  return v;
}

function runRS(F, budget, rnd) {
  let bx = 0, bz = 0, bv = 0;
  for (let i = 0; i < budget; i++) {
    const x = -H + rnd() * 2 * H, z = -H + rnd() * 2 * H;
    const v = evaluate(F, x, z);
    if (risk(F, x, z) < FEAS && v > bv) { bv = v; bx = x; bz = z; }
  }
  return { best: bv, x: bx, z: bz };
}

// fixed geometric cooling, single point, Metropolis acceptance
function runSA(F, budget, rnd) {
  let x = -H + rnd() * 2 * H, z = -H + rnd() * 2 * H;
  let cur = evaluate(F, x, z);
  let bx = x, bz = z, bv = risk(F, x, z) < FEAS ? cur : 0;
  const T0 = 0.30, T1 = 1e-3;
  for (let i = 1; i < budget; i++) {
    const T = T0 * Math.pow(T1 / T0, i / budget);
    const nx = clampv(x + gauss(rnd, 1.4 * T + 0.15), -H, H);
    const nz = clampv(z + gauss(rnd, 1.4 * T + 0.15), -H, H);
    const nv = evaluate(F, nx, nz);
    if (nv >= cur || rnd() < Math.exp((nv - cur) / Math.max(T, 1e-6))) { x = nx; z = nz; cur = nv; }
    if (risk(F, x, z) < FEAS && cur > bv) { bv = cur; bx = x; bz = z; }
  }
  return { best: bv, x: bx, z: bz };
}

// temperature-gated switch: coarse jump while T > T*, local search below
function runCOA(F, budget, rnd) {
  let x = -H + rnd() * 2 * H, z = -H + rnd() * 2 * H;
  let cur = evaluate(F, x, z);
  let bx = x, bz = z, bv = risk(F, x, z) < FEAS ? cur : 0;
  const Tstar = 0.15, T0 = 0.35;
  for (let i = 1; i < budget; i++) {
    const T = T0 * (1 - i / budget);
    let nx, nz;
    if (T > Tstar) {                     // exploration phase: large steps
      const a = rnd() * 2 * Math.PI, r = 2.2 + rnd() * 4.0;
      nx = clampv(x + Math.cos(a) * r, -H, H);
      nz = clampv(z + Math.sin(a) * r, -H, H);
    } else {                             // exploitation phase: small steps
      nx = clampv(x + gauss(rnd, 0.35), -H, H);
      nz = clampv(z + gauss(rnd, 0.35), -H, H);
    }
    const nv = evaluate(F, nx, nz);
    if (nv > cur || rnd() < 0.05) { x = nx; z = nz; cur = nv; }
    if (risk(F, x, z) < FEAS && cur > bv) { bv = cur; bx = x; bz = z; }
  }
  return { best: bv, x: bx, z: bz };
}

// one population, entropy annealed, no role separation, no scheduler
function runSPEA(F, budget, rnd) {
  const K = 12; // same population size as LRLS
  const pts = [];
  for (let k = 0; k < K; k++) {
    const x = -H + rnd() * 2 * H, z = -H + rnd() * 2 * H;
    pts.push({ x, z, v: evaluate(F, x, z) });
  }
  let bx = pts[0].x, bz = pts[0].z, bv = 0;
  for (const p of pts) if (risk(F, p.x, p.z) < FEAS && p.v > bv) { bv = p.v; bx = p.x; bz = p.z; }
  const used = K;
  const H0 = 1.0;
  for (let i = used; i < budget; i += K) {
    const hAnn = H0 * (1 - i / budget);         // entropy annealed globally
    for (const p of pts) {
      if (i >= budget) break;
      const step = 0.25 + 1.8 * hAnn;
      const nx = clampv(p.x + gauss(rnd, step), -H, H);
      const nz = clampv(p.z + gauss(rnd, step), -H, H);
      const nv = evaluate(F, nx, nz);
      if (nv > p.v || rnd() < 0.08 * hAnn) { p.x = nx; p.z = nz; p.v = nv; }
      if (risk(F, p.x, p.z) < FEAS && p.v > bv) { bv = p.v; bx = p.x; bz = p.z; }
    }
  }
  return { best: bv, x: bx, z: bz };
}

function coverageOf(ex) {
  let c = 0;
  for (let i = 0; i < ex.length; i++) if (ex[i] === 1) c++;
  return c / ex.length;
}

const out = { profiles: [], seeds: SEEDS, feasibilityGate: FEAS };

for (const prof of PROFILES) {
  const row = { name: prof.name, params: prof.params, methods: {} };
  for (const m of ['LRLS', 'RS', 'SA', 'COA-T', 'SP-EA']) row.methods[m] = [];
  const F = makeField(prof.params);
  const gmax = (() => {
    let g = 0;
    for (let i = 0; i <= CFG.N; i++) for (let j = 0; j <= CFG.N; j++) {
      const x = -H + i * 2 * H / CFG.N, z = -H + j * 2 * H / CFG.N;
      if (risk(F, x, z) < FEAS) g = Math.max(g, fval(F, x, z));
    }
    return g;
  })();
  F.gmax = gmax;
  row.gmax = +gmax.toFixed(4);
  globalThis.THR95 = 0.95 * gmax;
  globalThis.THR99 = 0.99 * gmax;

  for (const seed of SEEDS) {
    // LRLS reference run under this seed
    globalThis.SEED = seed;
    resetEV();
    const res = simulate(prof.params);
    const last = res.timeline[res.timeline.length - 1];
    const lrlsBudget = EV.n;
    row.methods.LRLS.push({
      seed, budget: lrlsBudget,
      best: +EV.best.toFixed(4), firstEval: EV.first, vio: EV.vio,
      n95: EV.n95, n99: EV.n99, vioAt99: EV.vioAt99,
      coverage: +coverageOf(last.ex).toFixed(4),
    });

    // baselines, budget-matched
    for (const [name, fn] of [['RS', runRS], ['SA', runSA], ['COA-T', runCOA], ['SP-EA', runSPEA]]) {
      resetEV();
      const rnd = mulberry32(seed * 7919 + 13);
      const r = fn(F, lrlsBudget, rnd);
      row.methods[name].push({
        seed, budget: lrlsBudget,
        best: +EV.best.toFixed(4), firstEval: EV.first, vio: EV.vio,
        n95: EV.n95, n99: EV.n99, vioAt99: EV.vioAt99,
        coverage: null,
      });
    }
    process.stderr.write('.');
  }
  out.profiles.push(row);
  process.stderr.write(' ' + prof.name + '\n');
}

// --- aggregate: mean ± std over seeds ---
function stats(a) {
  const n = a.length;
  const mean = a.reduce((s, v) => s + v, 0) / n;
  const sd = Math.sqrt(a.reduce((s, v) => s + (v - mean) ** 2, 0) / Math.max(n - 1, 1));
  return { mean: +mean.toFixed(4), sd: +sd.toFixed(4) };
}

out.summary = out.profiles.map(p => {
  const s = { name: p.name, gmax: p.gmax, methods: {} };
  for (const [m, runs] of Object.entries(p.methods)) {
    const h95 = runs.filter(r => r.n95 > 0).map(r => r.n95);
    const h99 = runs.filter(r => r.n99 > 0).map(r => r.n99);
    s.methods[m] = {
      best: stats(runs.map(r => r.best)),
      vio: stats(runs.map(r => r.vio)),
      n95: h95.length ? stats(h95) : { mean: null, sd: null },
      n99: h99.length ? stats(h99) : { mean: null, sd: null },
      vioAt99: h99.length ? stats(runs.filter(r => r.n99 > 0).map(r => r.vioAt99)) : { mean: null, sd: null },
      hit95: h95.length,
      hit99: h99.length,
      coverage: stats(runs.filter(r => r.coverage !== null).map(r => r.coverage)),
    };
  }
  return s;
});

console.log(JSON.stringify(out, null, 1));
