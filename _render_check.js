// 結合を考慮した「実際の見た目」を再現する
const fs = require('fs');
const ExcelJS = require('./node_modules/exceljs');

(async () => {
  const res = await fetch('http://localhost:3001/api/delivery/hearing-xlsx', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sheets: ['必須確認①'], info: {}, prefill: {} }),
  });
  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync('_render.xlsx', buf);
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);
  const ws = wb.getWorksheet('必須確認①');

  // 結合の「左上セル」だけを拾う
  const merges = ws.model.merges || [];
  const slave = new Set();
  const master = {};
  for (const m of merges) {
    const [a, b] = m.split(':');
    const col = s => s.match(/[A-Z]+/)[0];
    const row = s => parseInt(s.match(/\d+/)[0], 10);
    const c2n = c => c.split('').reduce((t, ch) => t * 26 + ch.charCodeAt(0) - 64, 0);
    const r1 = row(a), c1 = c2n(col(a)), c2 = c2n(col(b));
    master[`${r1}_${c1}`] = c2 - c1 + 1;
    for (let c = c1 + 1; c <= c2; c++) slave.add(`${r1}_${c}`);
  }

  console.log('=== Excelで実際に見える内容 ===');
  ws.eachRow((r, i) => {
    if (i > 14) return;
    const cells = [];
    r.eachCell({ includeEmpty: false }, (c, col) => {
      if (slave.has(`${i}_${col}`)) return;
      const v = String(c.value ?? '').trim().replace(/\n/g, ' ');
      if (!v) return;
      const span = master[`${i}_${col}`];
      const colName = String.fromCharCode(64 + col);
      cells.push(`[${colName}${span ? `(${span}列結合)` : ''}] ${v.slice(0, 54)}`);
    });
    if (cells.length) console.log(`${String(i).padStart(2)}| ${cells.join('   ')}`);
  });
  console.log('\n結合数:', merges.length);
})();
