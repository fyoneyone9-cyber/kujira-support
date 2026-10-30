// 生成xlsxを「見た目」に近い形で出力し、雛形CSVと並べて比較する
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
  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync('_preview.xlsx', buf);
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);
  const ws = wb.getWorksheet('必須確認①');
  console.log('=== 生成Excel（必須確認①） rows=%d ===\n', ws.rowCount);
  ws.eachRow((r, i) => {
    // 結合を考慮してテキストと回答欄を抽出
    let text = '', ans = '';
    r.eachCell({ includeEmpty: false }, (c, col) => {
      const v = String(c.value ?? '').replace(/\n/g, ' ').trim();
      if (!v) return;
      if (v === '□' || v === '✔') ans = v;
      else if (!text) text = v;
    });
    if (!text && !ans) return;
    const pad = text.length > 70 ? text.slice(0, 70) + '…' : text;
    console.log(`${String(i).padStart(2)}| ${pad.padEnd(72)} ${ans}`);
  });
})();
