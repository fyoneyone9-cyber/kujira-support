// 最終確認: 雛形CSVとExcel出力のセル位置が一致するか
const fs = require('fs');
const ExcelJS = require('./node_modules/exceljs');

const SHEETS = ['必須確認①', '必須確認②', '必須確認③', 'PMS',
  'スマートロック①', '事前チェックイン', 'カードキー', 'プリンタ'];

(async () => {
  const res = await fetch('http://localhost:3001/api/delivery/hearing-xlsx', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sheets: SHEETS,
      info: { client: '株式会社ビジョン', address: '兵庫県淡路市岩屋2604', contact: '石川様', due: '2026-12-01', equipment: 'PMS suitebook、スマートロック EPIC' },
      prefill: { 'スマートロック': 'TRUE', 'PMS': 'TRUE' },
    }),
  });
  console.log('status:', res.status);
  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync('_final.xlsx', buf);
  console.log('bytes:', buf.length);

  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);
  console.log('\n--- シート一覧 ---');
  wb.eachSheet(ws => console.log(`  ${ws.name.padEnd(16)} rows=${ws.rowCount}`));

  const ws = wb.getWorksheet('必須確認①');
  console.log('\n--- 必須確認① セル位置 ---');
  ws.eachRow((r, i) => {
    if (i > 20) return;
    const cs = [];
    r.eachCell({ includeEmpty: false }, (c, col) => {
      const v = String(c.value ?? '').replace(/\n/g, ' ').trim().slice(0, 30);
      if (v) cs.push(`${String.fromCharCode(64 + col)}=${v}`);
    });
    if (cs.length) console.log(`${String(i).padStart(2)}| ${cs.join(' ; ')}`);
  });

  const ansCols = new Set();
  ws.eachRow(r => r.eachCell({ includeEmpty: false }, (c, col) => {
    if (String(c.value) === '□') ansCols.add(col);
  }));
  console.log('\n回答欄(□)の列:', [...ansCols], '← 12(L列)が正');
})();
