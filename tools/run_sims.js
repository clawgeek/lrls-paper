// Headless data extraction for LRLS reference simulation.
// Usage: node run_sims.js > sim_data.json
const fs = require('fs');
const path = require('path');
const core = fs.readFileSync(path.join(__dirname, 'solver_core.js'), 'utf8');
const fn = new Function(core + '\nreturn simulate;')();
// Four operating profiles (same RNG seed per run; deterministic)
const profiles = [
  { name: 'P1-easy',      params: { lambdaE: .35, risk: .25, complexity: .20, stress: 0    } },
  { name: 'P2-default',   params: { lambdaE: .35, risk: .55, complexity: .50, stress: 0    } },
  { name: 'P3-highrisk',  params: { lambdaE: .30, risk: .68, complexity: .62, stress: .30 } },
  { name: 'P4-extreme',   params: { lambdaE: .15, risk: .90, complexity: .85, stress: .90 } },
];
const out = { profiles: [] };
for (const p of profiles) {
  const res = fn(p.params);
  // Per-tick metrics (every 5 ticks to keep file small)
  const series = [];
  let cumVio = 0;
  for (const fr of res.timeline) {
    cumVio += fr.m.violations;
    if (fr.t % 5 === 0) {
      series.push({
        t: fr.t,
        best: +fr.m.bestScore.toFixed(4),
        gmax: +fr.m.gmax.toFixed(4),
        coverage: +fr.m.coverage.toFixed(4),
        entropy: +fr.m.entropy.toFixed(4),
        reward: +fr.m.reward.toFixed(3),
        NC: fr.m.NC, NB: fr.m.NB,
        discovered: fr.m.discovered, reefs: fr.m.reefs,
        abandoned: fr.m.abandoned,
        vio: cumVio,
        solved: fr.m.solved
      });
    }
  }
  // Final occupancy grid + reef/cave snapshot (default profile only, for map fig)
  let map = null;
  if (p.name === 'P2-default') {
    const last = res.timeline[res.timeline.length - 1];
    // reconstruct ex from last frame? timeline stores ex per frame
    map = {
      ex: Array.from(last.ex),
      N: 22,
      reefs: last.reefs.map(r => ({ x: +r.x.toFixed(2), z: +r.z.toFixed(2), score: +r.score.toFixed(3) })),
      caves: last.caves.map(c => ({ x: +c.x.toFixed(2), z: +c.z.toFixed(2), state: c.state })),
      peaks: res.F.peaks.map(pk => ({ x: pk.x, z: pk.z, a: pk.a, s: pk.s })),
      hazards: res.F.hazards.map(h => ({ x: h.x, z: h.z, r: +h.r.toFixed(2) })),
      trailsC: res.trails.filter(tr => tr.kind === 'C').map(tr => ({ x: +tr.x.toFixed(2), z: +tr.z.toFixed(2) })),
      trailsB: res.trails.filter(tr => tr.kind === 'B').map(tr => ({ x: +tr.x.toFixed(2), z: +tr.z.toFixed(2) }))
    };
  }
  // Summary stats
  const firstReef = res.timeline.find(fr => fr.m.reefs > 0);
  const reportDone = res.timeline.find(fr => (fr.m.taskDone && fr.m.taskDone.REPORT));
  out.profiles.push({
    name: p.name,
    params: p.params,
    gmax: +res.gmax.toFixed(4),
    finalBest: +(res.timeline[res.timeline.length - 1].m.bestScore).toFixed(4),
    firstFeasibleT: firstReef ? firstReef.t : -1,
    reportDoneT: reportDone ? reportDone.t : -1,
    totalViolations: cumVio,
    reefsFinal: res.timeline[res.timeline.length - 1].m.reefs,
    abandonedFinal: res.timeline[res.timeline.length - 1].m.abandoned,
    series, map
  });
}
fs.writeFileSync(path.join(__dirname, 'sim_data.json'), JSON.stringify(out));
console.log('written sim_data.json');
for (const p of out.profiles) {
  console.log(p.name, 'gmax=' + p.gmax, 'best=' + p.finalBest, 'first=' + p.firstFeasibleT,
    'report=' + p.reportDoneT, 'vio=' + p.totalViolations, 'reefs=' + p.reefsFinal, 'aband=' + p.abandonedFinal);
}
