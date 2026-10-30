// 結合が復元され、重複が消えたか検証する
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
  fs.writeFileSync('_merged.xlsx', buf);
  console.log('status:', res.status, 'bytes:', buf.length);

  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);
  const ws = wb.getWorksheet('必須確認①');

  console.log('\n--- 各行の実セル（結合後）---');
  ws.eachRow((r, i) => {
    if (i > 14) return;
    const cs = [];
    r.eachCell({ includeEmpty: false }, (c, col) => {
      const v = String(c.value ?? '').replace(/\n/g, ' ').trim();
      if (v) cs.push(`${String.fromCharCode(64 + col)}="${v.slice(0, 44)}"`);
    });
    console.log(`${String(i).padStart(2)}| ${cs.join('  ')}`);
  });

  // 重複チェック
  let dupRows = 0;
  ws.eachRow(r => {
    const vals = [];
    r.eachCell({ includeEmpty: false }, c => {
      const v = String(c.value ?? '').trim();
      if (v && v !== '□' && v !== '✔') vals.push(v);
    });
    const uniq = new Set(vals);
    if (vals.length > 1 && uniq.size < vals.length) dupRows++;
  });
  console.log('\n同じ文字列が重複している行:', dupRows, '← 0が正');
  console.log('結合セル数:', Object.keys(ws._merges || {}).length);
})();
