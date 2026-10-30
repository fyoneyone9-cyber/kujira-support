// ダイアログHTMLのチェック反映をDOMモックで検証する
const fs = require('fs');
const html = fs.readFileSync('public/docs/hearing-gas-dialog.html', 'utf8');

// id属性を全部拾って、テキスト欄とチェックボックスを分類
const inputs = [...html.matchAll(/<input([^>]*)>/g)].map(m => {
  const a = m[1];
  const id = (a.match(/id="([^"]+)"/) || [])[1];
  const type = (a.match(/type=(\w+)|type="([^"]+)"/) || [])[0] || '';
  return { id, checkbox: /checkbox/.test(type) };
}).filter(x => x.id);

const texts = inputs.filter(x => !x.checkbox).map(x => x.id);
const checks = inputs.filter(x => x.checkbox).map(x => x.id);
console.log('テキスト欄:', texts.join(', '));
console.log('チェック欄:', checks.join(', '));

const conflict = texts.filter(t => checks.includes(t));
console.log('\nid衝突:', conflict.length ? conflict : 'なし ← 正常');

// JS が chk_ 付きで参照しているか
const usesChk = /getElementById\('chk_' \+ k\)/.test(html);
console.log('JSがchk_参照:', usesChk ? 'OK' : '❌ NG');

// KEYS と チェックid が対応するか
const KEYS = (html.match(/var KEYS = \[([^\]]+)\]/) || [])[1]
  .split(',').map(s => s.trim().replace(/'/g, ''));
const missing = KEYS.filter(k => !checks.includes('chk_' + k));
console.log('KEYS:', KEYS.length, '件 / 対応しないもの:', missing.length ? missing : 'なし ← 正常');

// label の for が合っているか
const fors = [...html.matchAll(/for="([^"]+)"/g)].map(m => m[1]);
const badFor = fors.filter(f => !checks.includes(f) && !texts.includes(f));
console.log('不正なlabel for:', badFor.length ? badFor : 'なし ← 正常');
