// 生成されたExcelの実際の見え方を、雛形CSVと並べて確認する
const fs = require('fs');
const path = require('path');
const ExcelJS = require('./node_modules/exceljs');

const DL = 'C:\\Users\\fyone\\Downloads';

function parseCSV(text) {
  const rows = []; let row = [], cur = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) { if (c === '"') { if (text[i + 1] === '"') { cur += '"'; i++; } else q = false; } else cur += c; }
    else if (c === '"') q = true;
    else if (c === ',') { row.push(cur); cur = ''; }
    else if (c === '\n') { row.push(cur); rows.push(row); row = []; cur = ''; }
    else if (c !== '\r') cur += c;
  }
  if (cur || row.length) { row.push(cur); rows.push(row); }
  return rows;
}
const CN = i => String.fromCharCode(65 + i);

(async () => {
  const res = await fetch('http://localhost:3001/api/delivery/hearing-xlsx', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sheets: ['必須確認①'], info: { client: 'テスト社' }, prefill: {} }),
  });
  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync('_inspect.xlsx', buf);
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);
  const ws = wb.getWorksheet('必須確認①');

  const f = fs.readdirSync(DL).find(x => x.includes(' - 必須確認①.csv'));
  const src = parseCSV(fs.readFileSync(path.join(DL, f), 'utf8').replace(/^\uFEFF/, ''));

  console.log('==== 雛形CSV ====');
  src.slice(0, 10).forEach((r, i) => {
    const s = r.map((c, j) => c.trim() ? `${CN(j)}:${c.trim().replace(/\n/g, '⏎').slice(0, 26)}` : '').filter(Boolean);
    console.log(`${String(i + 1).padStart(2)}| ${s.join(' ')}`);
  });

  console.log('\n==== 生成Excel ====');
  ws.eachRow((r, i) => {
    if (i > 10) return;
    const s = [];
    r.eachCell({ includeEmpty: false }, (c, col) => {
      const v = String(c.value ?? '').trim().replace(/\n/g, '⏎');
      if (v) s.push(`${CN(col - 1)}:${v.slice(0, 26)}`);
    });
    console.log(`${String(i).padStart(2)}| ${s.join(' ')}`);
  });

  console.log('\n==== 結合セル ====');
  const m = ws.model.merges || [];
  console.log(m.length ? m.slice(0, 12).join(' , ') : '(なし)');
  console.log('\n列数:', ws.columnCount, '行数:', ws.rowCount);
})();
