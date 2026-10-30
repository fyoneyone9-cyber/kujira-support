// [OVERWRITE_AUDIT_V1 2026-10-29]
// 「手動入力が再取込で上書きされる」危険が他にも残っていないかを全フィールドで監査する。
//
// 判定ロジック:
//   A = import-csv が upsert で送るキーの集合（= 毎回CSV値で上書きされる列）
//   B = UI(page.tsx) が patch(id, {...}) で書き込むキーの集合（= 手動入力）
//   A ∩ B = 「手動で入れても再取込で消える列」= 危険
const fs = require('fs');
const path = require('path');

const impSrc = fs.readFileSync(path.join(__dirname, 'src/app/api/delivery/import-csv/route.ts'), 'utf8');
const pageSrc = fs.readFileSync(path.join(__dirname, 'src/app/(app)/delivery/page.tsx'), 'utf8');

// --- A: import が送るキー（items.push({...}) の中身を取る）
const pushIdx = impSrc.indexOf('items.push({');
const pushEnd = impSrc.indexOf('})', pushIdx);
const pushBlock = impSrc.slice(pushIdx, pushEnd);
const A = new Set();
for (const m of pushBlock.matchAll(/^\s*([a-z0-9_]+)\s*[,:]/gmi)) A.add(m[1]);
// shorthand (変数名そのまま) も拾う
for (const m of pushBlock.matchAll(/^\s*([a-z0-9_]+)\s*,\s*$/gmi)) A.add(m[1]);
// 一括 update のキー（missing_in_last_import 等）
for (const m of impSrc.matchAll(/\.update\(\{\s*([a-z0-9_]+)\s*:/gi)) A.add(m[1]);

// --- B: UI が patch() で書くキー
const B = new Set();
for (const m of pageSrc.matchAll(/patch\(\s*[a-z0-9_.]+\s*,\s*\{([^}]*)\}/gi)) {
  for (const kk of m[1].matchAll(/([a-z0-9_]+)\s*:/gi)) B.add(kk[1]);
  for (const kk of m[1].matchAll(/\[\s*([a-z0-9_]+)\s*\]\s*:/gi)) B.add('(dynamic:' + kk[1] + ')');
}
// PATCH body を直接組んでいる箇所
for (const m of pageSrc.matchAll(/body:\s*JSON\.stringify\(\{\s*id\s*,\s*([^}]*)\}/gi)) {
  for (const kk of m[1].matchAll(/([a-z0-9_]+)\s*:/gi)) B.add(kk[1]);
  for (const kk of m[1].matchAll(/^\s*([a-z0-9_]+)\s*[,}]/gmi)) B.add(kk[1]);
}

console.log('=== A: import-csv が毎回上書きする列 ===');
console.log('  ' + [...A].sort().join(', '));
console.log('\n=== B: UI が手動で書き込む列 ===');
console.log('  ' + [...B].sort().join(', '));

const danger = [...B].filter(k => A.has(k));
console.log('\n=== A ∩ B : 手動入力が再取込で消える列（危険） ===');
if (danger.length === 0) console.log('  なし  -> OK');
else for (const d of danger) console.log('  🔴 ' + d);

// dashboard_todos が import 側に無いことの確認（手動入力の安全地帯）
console.log('\ndashboard_todos を import が書くか:', A.has('dashboard_todos') ? '🔴 YES' : 'NO -> OK');
process.exit(danger.length ? 1 : 0);
