// 15行目(現金支払い)が実際にどうなっているか、全セルを生で見る
const fs = require('fs');
const ExcelJS = require('./node_modules/exceljs');

(async () => {
  const res = await fetch('http://localhost:3001/api/delivery/hearing-xlsx', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sheets: ['必須確認①'], info: {}, prefill: {} }),
  });
  const buf = Buffer.from(await res.arrayBuffer());
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);
  const ws = wb.getWorksheet('必須確認①');
  for (const i of [14, 15, 16, 17]) {
    const r = ws.getRow(i);
    const cells = [];
    r.eachCell({ includeEmpty: false }, (c, col) => {
      cells.push(`${col}:${String(c.value ?? '').replace(/\n/g, ' ').slice(0, 44)}`);
    });
    console.log(`row${i}: ${cells.join(' | ')}`);
  }
  // 定義側の該当行
  const defs = require('./src/lib/hearingSheetDefs.ts.json' in {} ? '' : './_defs_tmp.json');
})().catch(e => console.log('ERR', e.message));
