// Push the LRLS-paper kit to GitHub via the Git Data API.
// git push is blocked by the local proxy; gh api works.
// Usage: node tools/push_github.js <owner/repo>
const fs = require('fs');
const os = require('os');
const path = require('path');
const { execFileSync } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const REPO = process.argv[2] || 'clawgeek/lrls-paper';
const SKIP = new Set(['.git', 'node_modules']);
let tmpN = 0;

function gh(method, endpoint, body) {
  const args = ['api', '--method', method, endpoint];
  let tmp;
  if (body !== undefined) {
    tmp = path.join(os.tmpdir(), 'lrls_gh_' + (++tmpN) + '_' + Date.now() + '.json');
    fs.writeFileSync(tmp, JSON.stringify(body));
    args.push('--input', tmp);
  }
  try {
    const out = execFileSync('gh', args, { encoding: 'utf8', maxBuffer: 64 * 1024 * 1024 });
    return out.trim() ? JSON.parse(out) : {};
  } finally {
    if (tmp) fs.unlinkSync(tmp);
  }
}

function blob(file) {
  const content = fs.readFileSync(file).toString('base64');
  const r = gh('POST', `repos/${REPO}/git/blobs`, { content, encoding: 'base64' });
  process.stdout.write('.');
  return r.sha;
}

function buildTree(dir) {
  const entries = [];
  for (const name of fs.readdirSync(dir).sort()) {
    if (SKIP.has(name) || name.startsWith('_edge') || name.startsWith('_shot') || name.endsWith('.png~')) continue;
    const full = path.join(dir, name);
    const st = fs.statSync(full);
    if (st.isDirectory()) {
      entries.push({ path: name, mode: '040000', type: 'tree', sha: buildTree(full) });
    } else {
      entries.push({ path: name, mode: '100644', type: 'blob', sha: blob(full) });
    }
  }
  return gh('POST', `repos/${REPO}/git/trees`, { tree: entries }).sha;
}

function main() {
  console.log('repo:', REPO);
  // ensure the repo has an initial commit on main (empty repos cannot take blobs first)
  let base;
  try {
    base = gh('GET', `repos/${REPO}/git/ref/heads/main`).object.sha;
    console.log('existing main:', base.slice(0, 8));
  } catch (e) {
    console.log('creating initial commit ...');
    const init = gh('PUT', `repos/${REPO}/contents/README.md`, {
      message: 'Initial commit',
      content: Buffer.from('# LRLS-v1.1 preprint kit\n').toString('base64'),
    });
    base = init.commit.sha;
  }

  console.log('uploading blobs and building tree ...');
  const tree = buildTree(ROOT);
  console.log('\ntree:', tree.slice(0, 8));

  const commit = gh('POST', `repos/${REPO}/git/commits`, {
    message: 'LRLS-v1.1 preprint: bilingual paper, LaTeX source, submission metadata, reference simulator',
    tree,
    parents: [base],
  });
  gh('PATCH', `repos/${REPO}/git/refs/heads/main`, { sha: commit.sha, force: false });
  console.log('commit:', commit.sha.slice(0, 8));

  // tag + release on this commit
  try {
    gh('POST', `repos/${REPO}/git/refs`, { ref: 'refs/tags/v1.0', sha: commit.sha });
    console.log('tag v1.0 created');
  } catch (e) { console.log('tag step:', e.message.split('\n')[0]); }

  const notes = [
    '## LRLS-v1.1 — Preprint v1.0 (2026-11-05)',
    '',
    'Bilingual specification + deterministic reference simulation.',
    '',
    '- `paper/lrls-v1.1-en.pdf` — English manuscript (9 pp)',
    '- `paper/lrls-v1.1-zh.pdf` — Chinese manuscript (8 pp, for ChinaXiv)',
    '- `paper/source/main.tex` — arXiv-ready LaTeX source',
    '- `paper/assets/lrls-sim.html` — offline single-file simulator (1100 ticks, 22x22 terrain, 22 agents)',
    '- `metadata/` — ready-to-paste submission forms for Zenodo / ChinaXiv / TechRxiv / arXiv',
    '',
    'This is a specification and reference implementation, **not** a claim of algorithmic superiority.',
    'No learned policy, no multi-seed statistics, no baseline comparison, no physical-robot experiment.',
    'See Section 6 (Limitations).',
    '',
    'Text: CC BY 4.0 · Code: MIT · Author: Jason Sang (桑杰逊)',
  ].join('\n');
  try {
    const rel = gh('POST', `repos/${REPO}/releases`, {
      tag_name: 'v1.0', name: 'LRLS-v1.1 Preprint v1.0',
      body: notes, draft: false, prerelease: false, target_commitish: commit.sha,
    });
    console.log('release:', rel.html_url);
  } catch (e) { console.log('release step:', e.message.split('\n')[0]); }

  const listing = gh('GET', `repos/${REPO}/git/trees/main?recursive=1`);
  console.log('\n=== files on main (' + listing.tree.length + ') ===');
  for (const t of listing.tree) if (t.type === 'blob') console.log('  ' + t.path);
}
main();
