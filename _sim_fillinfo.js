// Apps Script の fillInfo が実際のシートで動くかシミュレートする
const fs = require('fs');
const defs = JSON.parse(
  fs.readFileSync('src/lib/hearingSheetDefs.ts', 'utf8').split('= ')[1].trim()
);
const rows = defs['必須確認②'];

const p = {
  client: '株式会社ビジョン',
  contact: '石川様',
  property: '〒656-2401 兵庫県淡路市岩屋2604',
  tel: '0799-00-0000',
};

// --- fillInfo と同じロジック ---
let zip = '', addr = p.property || '';
const m = addr.match(/〒?\s*(\d{3}-?\d{4})/);
if (m) { zip = m[1]; addr = addr.replace(m[0], '').trim(); }
console.log('郵便番号抽出:', zip, '/ 住所:', addr);

const MAP = [
  ['組織名', p.client],
  ['DMSにログインされる方のお名前', p.contact],
  ['物件名', addr],
  ['物件の住所', addr],
  ['物件の郵便番号', zip],
  ['お電話番号', p.tel],
];

let ansCol = 0;
for (let r = 0; r < Math.min(6, rows.length); r++) {
  for (let c = 0; c < rows[r].length; c++) {
    if (String(rows[r][c]).indexOf('ご回答欄') >= 0) { ansCol = c + 1; break; }
  }
  if (ansCol) break;
}
console.log('ご回答欄の列:', ansCol, '(', String.fromCharCode(64 + ansCol), ')');
if (!ansCol) { console.log('❌ 回答欄が見つからない'); process.exit(0); }

let n = 0;
for (let r2 = 0; r2 < rows.length; r2++) {
  const rowText = rows[r2].join(' ');
  for (const [key, val] of MAP) {
    if (!val) continue;
    if (rowText.indexOf(key) >= 0) {
      console.log(`  行${r2 + 1} "${rows[r2].find(x => x && x.length > 2) || ''}".slice -> ${key} = ${val}`);
      n++;
      break;
    }
  }
}
console.log('\n入力される件数:', n, '← 6前後が正');
