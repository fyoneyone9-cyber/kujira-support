// ④担当者氏名ブロックのラベルと値を直接確認する
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

  console.log('=== 1列目のラベル一覧（空白除去後）===');
  for (let i = 8; i <= 66; i++) {
    const v = txt(ws.getRow(i).getCell(1).value).trim();
    if (v) console.log(`  行${String(i).padStart(2)}: "${v.replace(/[\s　]+/g, '')}"`);
  }

  console.log('\n=== 行28-34 の 7〜36列 ===');
  for (let i = 28; i <= 34; i++) {
    const r = ws.getRow(i);
    const seen = new Set();
    const out = [];
    for (let c = 7; c <= 36; c++) {
      const v = txt(r.getCell(c).value).trim();
      if (v && !seen.has(v)) { seen.add(v); out.push(`[${c}]${v}`); }
    }
    if (out.length) console.log(`  行${i}: ${out.join('  ')}`);
  }
})();
