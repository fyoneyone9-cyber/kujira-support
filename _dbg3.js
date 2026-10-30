// blockRows(/担当者氏名/) が何行返すかを再現する
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

  const grid = {};
  ws.eachRow((row, ri) => {
    grid[ri] = {};
    row.eachCell({ includeEmpty: false }, (c, ci) => {
      const t = txt(c.value).trim();
      if (t) grid[ri][ci] = t;
    });
  });
  const rowNums = Object.keys(grid).map(Number).sort((a, b) => a - b);

  const blockRows = re => rowNums.filter(ri => re.test((grid[ri][1] || '').replace(/[\s　]+/g, '')));

  const hit = blockRows(/担当者氏名/);
  const out = { matchedRows: hit, col7: {} };
  for (const ri of hit) out.col7[ri] = grid[ri][7] || '(空)';

  // 各種パターンも試す
  out.tries = {
    '担当者氏名': blockRows(/担当者氏名/).length,
    '担当者': blockRows(/担当者/).length,
    '④': blockRows(/④/).length,
    'および連絡先': blockRows(/および連絡先/).length,
  };
  fs.writeFileSync('_dbg3.json', JSON.stringify(out, null, 1), 'utf8');
  console.log('matched rows:', hit.length, '/ tries:', JSON.stringify(out.tries));
})();
