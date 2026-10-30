// 全シートで重複が無いか最終検証する
const fs = require('fs');
const ExcelJS = require('./node_modules/exceljs');

const SHEETS = ['必須確認①', '必須確認②', '必須確認③', 'PMS',
  'スマートロック①', '事前チェックイン', 'カードキー', 'プリンタ',
  'シリンダー錠', 'ルームタブレット', '現金決済', '端末カード決済',
  'PayPay決済', 'デイユース', '補助金'];

(async () => {
  const res = await fetch('http://localhost:3001/api/delivery/hearing-xlsx', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sheets: SHEETS,
      info: { client: '株式会社ビジョン', address: '兵庫県淡路市岩屋2604', contact: '石川様', due: '2026-12-01', equipment: 'PMS suitebook、スマートロック EPIC、パスポートリーダー 1' },
      prefill: { 'スマートロック': 'TRUE', 'PMS': 'TRUE' },
    }),
  });
  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync('_all.xlsx', buf);
  console.log('status:', res.status, 'bytes:', buf.length);

  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);
  console.log('\n%-18s %-6s %-6s %s', 'シート', '行数', '重複行', '回答欄列');
  let totalDup = 0;
  wb.eachSheet(ws => {
    let dup = 0;
    const ansCols = new Set();
    ws.eachRow(r => {
      const vals = [];
      r.eachCell({ includeEmpty: false }, (c, col) => {
        const v = String(c.value ?? '').trim();
        if (v === '□' || v === '✔') { ansCols.add(col); return; }
        if (v) vals.push(v);
      });
      if (vals.length > 1 && new Set(vals).size < vals.length) dup++;
    });
    totalDup += dup;
    console.log(`  ${ws.name.padEnd(16)} ${String(ws.rowCount).padEnd(6)} ${String(dup).padEnd(6)} ${[...ansCols].join(',') || '-'}`);
  });
  console.log('\n重複行の合計:', totalDup, '← 0が正');
})();
