// 旧ロジックと新ロジックで削除結果を比較する
// 実データ（工程管理表111行）の区分配列を使う
const fs = require('fs');
const t = fs.readFileSync('src/lib/kouteiDef.ts', 'utf8');
const rows = JSON.parse(t.slice(t.indexOf('KOUTEI_ROWS: string[][] = ') + 26, t.indexOf('\n\n// 区分')).trim());

const cats = rows.map(r => (r[2] || '').trim());
// ビジョン社の想定: 共通/チェックインシステム/PMS/スマートロック/KIOSK/Surface/P400/PayCube/PayPay/スマホ/パスポート
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

// --- 旧ロジックを再現 ---
function oldLogic(delArr) {
  const removed = [];
  let i2 = delArr.length - 1;
  let guard = 0;
  while (i2 >= 0 && guard++ < 10000) {
    const end = delArr[i2];
    let start = end;
    while (i2 > 0 && delArr[i2 - 1] === start - 1) { i2--; start = delArr[i2]; }
    for (let r = start; r <= end; r++) removed.push(r);
    i2--;
  }
  return removed;
}
// --- 新ロジック ---
function newLogic(delArr) {
  const removed = [];
  for (let k = delArr.length - 1; k >= 0; k--) removed.push(delArr[k]);
  return removed;
}

const o = oldLogic([...del]).sort((a, b) => a - b);
const n = newLogic([...del]).sort((a, b) => a - b);
const want = [...del].sort((a, b) => a - b);

console.log('旧ロジックで削除される行数:', o.length);
console.log('新ロジックで削除される行数:', n.length);

const missedOld = want.filter(x => !o.includes(x));
const missedNew = want.filter(x => !n.includes(x));
console.log('\n旧: 取りこぼした行数 =', missedOld.length);
if (missedOld.length) {
  console.log('   残ってしまう区分:',
    [...new Set(missedOld.map(r => cats[r - 1]))].join(' / '));
}
console.log('新: 取りこぼした行数 =', missedNew.length, missedNew.length ? '' : '← 正常');
