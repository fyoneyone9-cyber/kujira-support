// [GAS_AUDIT_V1 2026-10-29]
// Apps Script 関連の整合性をまとめて検査する。
// 本日の事故（バージョン不一致 / 文字化け / 関数欠落）を再発させないためのゲート。
//
// 使い方:  node _audit_gas.js
//          終了コード 0 = OK / 1 = 問題あり
const fs = require('fs');
const vm = require('vm');

const G = 'public/docs/hearing-gas.js';
const D = 'public/docs/hearing-gas-dialog.html';
let ng = 0;
const fail = m => { console.log('  NG  ' + m); ng++; };
const ok = m => console.log('  OK  ' + m);

const g = fs.readFileSync(G, 'utf8');
const d = fs.readFileSync(D, 'utf8');

console.log('=== 1. バージョン整合 ===');
const gv = (g.match(/var GAS_VERSION = '([^']*)'/) || [])[1];
const dv = (d.match(/var DIALOG_VERSION = '([^']*)'/) || [])[1];
if (!gv) fail('GAS_VERSION が無い');
else if (!dv) fail('DIALOG_VERSION が無い');
else if (gv !== dv) fail(`不一致 GAS=${gv} / DIALOG=${dv}`);
else ok(`一致 ${gv}`);

console.log('\n=== 2. 文字化け検査 ===');
// 日本語の直後に単独の大文字ラテンが来るのは典型的な破損
const PAT = /[ぁ-んァ-ヶ一-龥][A-Z](?![A-Za-z0-9])/;
const PUA = /[\ue000-\uf8ff]/;
for (const [name, txt] of [['hearing-gas.js', g], ['dialog', d]]) {
  const bad = txt.split('\n')
    .map((l, i) => ({ n: i + 1, l }))
    .filter(x => PUA.test(x.l) || PAT.test(x.l));
  if (bad.length) {
    fail(`${name} に疑わしい箇所 ${bad.length}件 (先頭 L${bad[0].n})`);
    bad.slice(0, 3).forEach(x => console.log(`        L${x.n}: ${x.l.trim().slice(0, 60)}`));
  } else ok(`${name} 破損なし`);
}

console.log('\n=== 3. 関数の対応 ===');
const defined = new Set([...g.matchAll(/function\s+(\w+)\s*\(/g)].map(m => m[1]));
const need = ['onOpen', 'showDialog', 'getVersion', 'getSheetNames',
  'suggestSheets', 'createCopy', 'fillInfo', 'checkAuth'];
for (const f of need) {
  if (defined.has(f)) ok(`${f} 定義あり`);
  else fail(`${f} が未定義`);
}
// dialog が呼ぶ関数
const called = new Set([...d.matchAll(/probe\('(\w+)'/g)].map(m => m[1]));
for (const f of called) {
  if (!defined.has(f)) fail(`dialog が呼ぶ ${f} がコード側に無い`);
}

console.log('\n=== 4. JS構文 ===');
try { new vm.Script(g); ok('hearing-gas.js 構文OK'); }
catch (e) { fail('hearing-gas.js 構文エラー: ' + e.message); }
const m = d.match(/<script>([\s\S]*?)<\/script>/);
if (!m) fail('dialog に script ブロックが無い');
else {
  try { new vm.Script(m[1]); ok('dialog 構文OK'); }
  catch (e) { fail('dialog 構文エラー: ' + e.message); }
}

console.log('\n=== 5. 廃止要素の残骸 ===');
for (const [label, pat] of [
  ['frontci（フロントチェックイン）', /frontci/],
  ['固定チェックボックス chk_', /chk_pms/],
  ['PMS名の入力欄', /id="pms"/],
]) {
  if (pat.test(g) || pat.test(d)) fail(`${label} が残っている`);
  else ok(`${label} 除去済み`);
}

console.log(ng === 0 ? '\nRESULT: PASS' : `\nRESULT: FAIL (${ng}件)`);
process.exit(ng === 0 ? 0 : 1);
