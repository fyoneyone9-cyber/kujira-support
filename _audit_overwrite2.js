// [OVERWRITE_AUDIT_V2 2026-10-29]
// V1は「同名の列を両方が書いているか」しか見ておらず、import側のガード有無を
// 判定できなかった（status/delivery_due_date は実際にはガード済みなのに🔴と出る）。
// V2は「import が送る値が、既存の手動値を考慮しているか」まで見る。
const fs = require('fs');
const path = require('path');
const imp = fs.readFileSync(path.join(__dirname, 'src/app/api/delivery/import-csv/route.ts'), 'utf8');
const page = fs.readFileSync(path.join(__dirname, 'src/app/(app)/delivery/page.tsx'), 'utf8');

const pushIdx = imp.indexOf('items.push({');
const pushEnd = imp.indexOf('})', pushIdx);
const pushBlock = imp.slice(pushIdx, pushEnd);

const A = new Set();
for (const m of pushBlock.matchAll(/^\s*([a-z0-9_]+)\s*[,:]/gmi)) A.add(m[1]);
for (const m of imp.matchAll(/\.update\(\{\s*([a-z0-9_]+)\s*:/gi)) A.add(m[1]);

const B = new Set();
for (const m of page.matchAll(/patch\(\s*[a-z0-9_.]+\s*,\s*\{([^}]*)\}/gi))
  for (const kk of m[1].matchAll(/([a-z0-9_]+)\s*:/gi)) B.add(kk[1]);
for (const m of page.matchAll(/body:\s*JSON\.stringify\(\{\s*id\s*,\s*([^}]*)\}/gi))
  for (const kk of m[1].matchAll(/([a-z0-9_]+)\s*:/gi)) B.add(kk[1]);

// 既存値を読み出して考慮している列（ガードあり）を検出
const GUARDED = new Map();
// 1) existingStatusMap のような Map を使っているか
if (/existingStatusMap\.get\(item_key\)/.test(imp)) GUARDED.set('status', 'existingStatusMap で手動done維持');
if (/manualDueMap\.get\(item_key\)/.test(imp)) GUARDED.set('delivery_due_date', 'manualDueMap で手動納期優先');

const inter = [...B].filter(k => A.has(k));
console.log('A ∩ B（両方が書く列）:', inter.join(', ') || 'なし');
console.log('');
let bad = 0;
for (const k of inter) {
  if (GUARDED.has(k)) console.log(`  ✅ ${k.padEnd(20)} ガードあり: ${GUARDED.get(k)}`);
  else { bad++; console.log(`  🔴 ${k.padEnd(20)} ガード無し → 再取込で手動値が消える`); }
}
console.log('\ndashboard_todos を import が書くか:', A.has('dashboard_todos') ? '🔴 YES' : 'NO -> OK（手動入力の安全地帯）');
console.log(`\nRESULT: ${bad === 0 ? 'PASS - 手動入力が消える列は無し' : 'FAIL - 危険な列が ' + bad + ' 件'}`);
process.exit(bad ? 1 : 0);
