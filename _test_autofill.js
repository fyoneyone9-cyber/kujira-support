// 自動入力と全シート出力を検証する
const fs = require('fs');
const ExcelJS = require('./node_modules/exceljs');

const SHEETS = ['必須確認①', '必須確認②', '必須確認③', 'PMS',
  'スマートロック①', 'スマートロック②', '事前チェックイン', 'フロントチェックイン',
  'カードキー', 'シリンダー錠', 'プリンタ', 'ルームタブレット',
  '現金決済', '端末カード決済', 'PayPay決済'];

(async () => {
  const res = await fetch('http://localhost:3001/api/delivery/hearing-xlsx', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sheets: SHEETS,
      info: { client: '株式会社ビジョン', address: '〒656-2401 兵庫県淡路市岩屋2604', contact: '石川様', due: '2026-12-01', equipment: 'PMS suitebook、スマートロック EPIC' },
      prefill: { 'スマートロック': 'TRUE', 'PMS': 'TRUE' },
      fill: {
        '組織名': '株式会社ビジョン',
        'DMSにログインされる方のお名前': '石川様',
        '物件名': '兵庫県淡路市岩屋2604',
        '物件の住所': '兵庫県淡路市岩屋2604',
        '物件の郵便番号': '656-2401',
        'お電話番号': '0799-00-0000',
      },
    }),
  });
  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync('_autofill.xlsx', buf);
  console.log('status:', res.status, 'bytes:', buf.length);

  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);
  console.log('\n=== シート一覧 ===');
  wb.eachSheet(ws => {
    const empty = ws.rowCount <= 2 ? '  ← 空！' : '';
    console.log(`  ${ws.name.padEnd(18)} rows=${String(ws.rowCount).padEnd(5)}${empty}`);
  });

  const ws = wb.getWorksheet('必須確認②');
  console.log('\n=== 必須確認② 自動入力の確認 ===');
  ws.eachRow((r, i) => {
    if (i > 16) return;
    const cs = [];
    r.eachCell({ includeEmpty: false }, (c, col) => {
      const v = String(c.value ?? '').trim().replace(/\n/g, ' ');
      if (v) cs.push(`${String.fromCharCode(64 + col)}:${v.slice(0, 32)}`);
    });
    if (cs.length) console.log(`${String(i).padStart(2)}| ${cs.join('  ')}`);
  });
})();
