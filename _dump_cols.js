// 申込書の列番号を正確に把握する
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

  console.log('=== 費用明細行（品名と数量の列番号）===');
  for (let i = 10; i <= 42; i++) {
    const r = ws.getRow(i);
    const cs = [];
    r.eachCell({ includeEmpty: false }, (c, ci) => {
      const v = txt(c.value).trim().replace(/\n/g, ' ');
      if (v) cs.push(`[${ci}]${v.slice(0, 30)}`);
    });
    if (cs.length) console.log(`${String(i).padStart(3)}| ${cs.join(' ')}`);
  }

  console.log('\n=== 契約者情報ブロック（1〜12列のみ）===');
  for (let i = 8; i <= 66; i++) {
    const r = ws.getRow(i);
    const cs = [];
    r.eachCell({ includeEmpty: false }, (c, ci) => {
      if (ci > 22) return;
      const v = txt(c.value).trim().replace(/\n/g, ' ');
      if (v) cs.push(`[${ci}]${v.slice(0, 34)}`);
    });
    if (cs.length) console.log(`${String(i).padStart(3)}| ${cs.join(' ')}`);
  }
})();
