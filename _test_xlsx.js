// 生成されたxlsxの中身を検証する
const fs = require('fs');
const ExcelJS = require('./node_modules/exceljs');

(async () => {
  const res = await fetch('http://localhost:3001/api/delivery/hearing-xlsx', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sheets: ['必須確認①', '必須確認②', '必須確認③', 'PMS',
        'スマートロック①', 'スマートロック②', '事前チェックイン', 'フロントチェックイン'],
      info: {
        client: '株式会社ビジョン', address: '〒656-2401 兵庫県淡路市岩屋2604',
        contact: '石川様', due: '2026-12-01',
        equipment: 'PMS suitebook、スマートロック EPIC、パスポートリーダー 1',
      },
      prefill: { 'スマートロック': 'TRUE', 'PMS': 'TRUE', 'カードキー': 'FALSE' },
    }),
  });
  console.log('status:', res.status, res.headers.get('content-type'));
  if (!res.ok) { console.log(await res.text()); return; }
  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync('_test_out.xlsx', buf);
  console.log('bytes:', buf.length);

  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);
  console.log('\n--- シート一覧 ---');
  wb.eachSheet(ws => {
    console.log(`  ${ws.name.padEnd(16)} rows=${ws.rowCount} cols=${ws.columnCount}`);
  });
  const c = wb.getWorksheet('表紙');
  console.log('\n--- 表紙 ---');
  c.eachRow((r, i) => { if (i <= 8) console.log('  ', (r.getCell(1).value || '') + ': ' + String(r.getCell(2).value || '').slice(0, 60)); });
  const q1 = wb.getWorksheet('必須確認①');
  console.log('\n--- 必須確認① 先頭6行 ---');
  q1.eachRow((r, i) => {
    if (i <= 6) console.log('  ', r.values.slice(1).map(v => String(v ?? '').slice(0, 42)).join(' | '));
  });
})();
