// fill のキー照合が成立しているかをローカルで再現する
const fs = require('fs');
const defs = JSON.parse(
  fs.readFileSync('src/lib/hearingSheetDefs.ts', 'utf8').split('= ')[1].trim()
);
const d = defs['必須確認②'];

// ANS の検出（route.ts と同じロジック）
let ANS = 12;
for (const row of d.slice(0, 6)) {
  const idx = row.findIndex(c => c && c.includes('ご回答欄'));
  if (idx >= 0) { ANS = idx + 1; break; }
}
console.log('検出された ANS =', ANS, '(列', String.fromCharCode(64 + ANS), ')');

const fill = {
  '組織名': '株式会社ビジョン',
  'DMSにログインされる方のお名前': '石川様',
  '物件名': 'グランピングリゾートAwaji',
  '物件の住所': '兵庫県淡路市岩屋2604',
  '物件の郵便番号': '656-2401',
};

console.log('\n--- 各行のラベル照合 ---');
d.slice(0, 16).forEach((row, ri) => {
  const vals = [...row];
  const label = vals.find(v => v && v !== '□' && v !== '✔') || '';
  const key = Object.keys(fill).find(k => label.includes(k));
  if (label) {
    console.log(`行${String(ri).padStart(2)} label="${label.slice(0, 28)}" -> ${key ? '✅ ' + key + ' = ' + fill[key] : '×'}`);
  }
});
