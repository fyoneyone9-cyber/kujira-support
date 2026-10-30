// 生成xlsxの列位置が雛形どおりか検証する
const fs = require('fs');
const ExcelJS = require('./node_modules/exceljs');

(async () => {
  const res = await fetch('http://localhost:3001/api/delivery/hearing-xlsx', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sheets: ['必須確認①'],
      info: { client: '株式会社ビジョン', address: '兵庫県淡路市岩屋2604', contact: '石川様', due: '2026-12-01', equipment: 'PMS suitebook、スマートロック EPIC' },
      prefill: { 'スマートロック': 'TRUE', 'PMS': 'TRUE' },
    }),
  });
  console.log('status:', res.status);
  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync('_test_out2.xlsx', buf);
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);
  const ws = wb.getWorksheet('必須確認①');
  console.log('rows:', ws.rowCount, 'cols:', ws.columnCount);
  console.log('\n--- セル位置（列番号つき）---');
  ws.eachRow((r, i) => {
    if (i > 10) return;
    const cells = [];
    r.eachCell({ includeEmpty: false }, (c, col) => {
      const v = String(c.value ?? '').replace(/\n/g, ' ').slice(0, 36);
      if (v) cells.push(`${String.fromCharCode(64 + col)}列:${v}`);
    });
    console.log(`${String(i).padStart(2)}: ${cells.join(' | ')}`);
  });
  // 回答欄の列を確認
  let ansCols = new Set();
  ws.eachRow(r => r.eachCell({ includeEmpty: false }, (c, col) => {
    if (String(c.value) === '□') ansCols.add(col);
  }));
  console.log('\n回答欄(□)がある列:', [...ansCols], '← 12(L列)が正');
})();
