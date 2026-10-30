// 旧/新ロジックの削除結果を比較する
const fs = require('fs');
const t = fs.readFileSync('src/lib/kouteiDef.ts', 'utf8');
const s = t.indexOf('[', t.indexOf('KOUTEI_ROWS'));
// 対応する閉じ括弧を探す
let depth = 0, e = s;
for (; e < t.length; e++) {
  if (t[e] === '[') depth++;
  else if (t[e] === ']') { depth--; if (depth === 0) { e++; break; } }
}
const rows = JSON.parse(t.slice(s, e));
const cats = rows.map(r => (r[2] || '').trim());
console.log('総行数:', rows.length);

const keep = {};
['01.共通', '03.チェックインシステム', '04.PMS', '06.スマートロック', '08.KIOSK',
 '11.Surface', '13.P400', '14.PayCube', '15.PayPay', '16.スマホカード決済',
 '17.パスポートリーダー'].forEach(c => keep[c] = true);

const del = [];
for (let i = 3; i < cats.length; i++) {
  const c = cats[i];
  if (!c) continue;
  if (!keep[c]) del.push(i + 1);
}
console.log('削除すべき行数:', del.length);

function oldLogic(a) {
  const out = [];
  let i2 = a.length - 1, guard = 0;
  while (i2 >= 0 && guard++ < 10000) {
    const end = a[i2];
    let start = end;
    while (i2 > 0 && a[i2 - 1] === start - 1) { i2--; start = a[i2]; }
    for (let r = start; r <= end; r++) out.push(r);
    i2--;
  }
  return out;
}
const o = [...new Set(oldLogic([...del]))];
const n = [...del];
const missedOld = del.filter(x => !o.includes(x));
const extraOld = o.filter(x => !del.includes(x));

console.log('\n--- 旧ロジック ---');
console.log('  削除される行:', o.length);
console.log('  取りこぼし  :', missedOld.length);
if (missedOld.length) {
  const z = [...new Set(missedOld.map(r => cats[r - 1]))];
  console.log('  → 残ってしまう区分:', z.join(' / '));
}
console.log('  余計に消す  :', extraOld.length);
if (extraOld.length) {
  const z = [...new Set(extraOld.map(r => cats[r - 1]))];
  console.log('  → 消してはいけない区分:', z.join(' / '));
}

console.log('\n--- 新ロジック ---');
console.log('  削除される行:', n.length);
console.log('  取りこぼし  :', del.filter(x => !n.includes(x)).length, '← 0が正');
