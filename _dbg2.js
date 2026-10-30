// ④担当者ブロックの値を JSON で出す（文字化け回避）
const fs = require('fs');
const ExcelJS = require('./node_modules/exceljs');
const P = 'C:\\Users\\fyone\\Downloads\\【ADVANCED IOT スマートチェックイン】申込書_株式会社ビジョン御中_20261005.xlsx';

function txt(v) {
  if (v == null) return '';
  if (typeof v === 'object') {
    if (Array.isArray(v.richText)) return v.richText.map(r => r.text || '').join('');
    if (v.result !== undefined) return String(v.result);
    if (v.text !== undefined) return String(v.text);
    return '';
  }
  return String(v);
}

(async () => {
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.readFile(P);
  const ws = wb.worksheets.find(w => w.name.includes('申込'));
  const out = {};
  for (let i = 28; i <= 34; i++) {
    const r = ws.getRow(i);
    const seen = new Set(); const vals = [];
    for (let c = 7; c <= 36; c++) {
      const v = txt(r.getCell(c).value).trim();
      if (v && !seen.has(v)) { seen.add(v); vals.push({ col: c, v }); }
    }
    out[i] = { label: txt(r.getCell(1).value).trim().replace(/[\s　]+/g, ''), vals };
  }
  fs.writeFileSync('_dbg2.json', JSON.stringify(out, null, 1), 'utf8');
  console.log('wrote _dbg2.json');
})();
