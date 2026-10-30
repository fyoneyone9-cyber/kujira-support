// 申込書xlsxの構造を解析する
const ExcelJS = require('./node_modules/exceljs');
const P = 'C:\\Users\\fyone\\Downloads\\【ADVANCED IOT スマートチェックイン】申込書_株式会社ビジョン御中_20261005.xlsx';

(async () => {
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.readFile(P);
  console.log('=== シート一覧 ===');
  wb.eachSheet(ws => console.log(`  ${ws.name}  rows=${ws.rowCount} cols=${ws.columnCount}`));

  wb.eachSheet(ws => {
    console.log(`\n===== ${ws.name} =====`);
    const merges = ws.model.merges || [];
    const slave = new Set();
    for (const m of merges) {
      const [a, b] = m.split(':');
      const c2n = c => c.split('').reduce((t, ch) => t * 26 + ch.charCodeAt(0) - 64, 0);
      const r1 = parseInt(a.match(/\d+/)[0], 10), r2 = parseInt(b.match(/\d+/)[0], 10);
      const c1 = c2n(a.match(/[A-Z]+/)[0]), c2 = c2n(b.match(/[A-Z]+/)[0]);
      for (let r = r1; r <= r2; r++) for (let c = c1; c <= c2; c++) {
        if (!(r === r1 && c === c1)) slave.add(`${r}_${c}`);
      }
    }
    ws.eachRow((row, i) => {
      if (i > 80) return;
      const cs = [];
      row.eachCell({ includeEmpty: false }, (c, col) => {
        if (slave.has(`${i}_${col}`)) return;
        let v = c.value;
        if (v && typeof v === 'object') v = v.result ?? v.text ?? JSON.stringify(v);
        v = String(v ?? '').trim().replace(/\n/g, ' ');
        if (v) cs.push(`${String.fromCharCode(64 + col)}:${v.slice(0, 40)}`);
      });
      if (cs.length) console.log(`${String(i).padStart(3)}| ${cs.join('  ')}`);
    });
  });
})();
