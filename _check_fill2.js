// 自動入力が効いているか、結合を考慮して実セルだけ見る
const fs = require('fs');
const ExcelJS = require('./node_modules/exceljs');

(async () => {
  const res = await fetch('http://localhost:3001/api/delivery/hearing-xlsx', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      sheets: ['必須確認②'],
      info: {},
      prefill: {},
      fill: {
        '組織名': '株式会社ビジョン',
        'DMSにログインされる方のお名前': '石川様',
        '物件名': 'グランピングリゾートAwaji',
        '物件の住所': '兵庫県淡路市岩屋2604',
        '物件の郵便番号': '656-2401',
        'お電話番号': '0799-00-0000',
      },
    }),
  });
  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync('_fill2.xlsx', buf);
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);
  const ws = wb.getWorksheet('必須確認②');

  const merges = ws.model.merges || [];
  const slave = new Set();
  for (const m of merges) {
    const [a, b] = m.split(':');
    const c2n = c => c.split('').reduce((t, ch) => t * 26 + ch.charCodeAt(0) - 64, 0);
    const r1 = parseInt(a.match(/\d+/)[0], 10);
    const c1 = c2n(a.match(/[A-Z]+/)[0]), c2 = c2n(b.match(/[A-Z]+/)[0]);
    for (let c = c1 + 1; c <= c2; c++) slave.add(`${r1}_${c}`);
  }

  console.log('=== 実セルのみ（結合の従属セルを除外）===');
  ws.eachRow((r, i) => {
    if (i > 17) return;
    const cs = [];
    r.eachCell({ includeEmpty: false }, (c, col) => {
      if (slave.has(`${i}_${col}`)) return;
      const v = String(c.value ?? '').trim().replace(/\n/g, ' ');
      if (v) cs.push(`${String.fromCharCode(64 + col)}:${v.slice(0, 36)}`);
    });
    if (cs.length) console.log(`${String(i).padStart(2)}| ${cs.join('  ||  ')}`);
  });
})();
