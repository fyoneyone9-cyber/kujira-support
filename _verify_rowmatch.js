// 行番号が雛形CSVと一致するか検証する
const fs = require('fs');
const ExcelJS = require('./node_modules/exceljs');

const CSV = 'C:\\Users\\fyone\\Downloads\\ヒアリングシート（ひな形・閲覧用） - 必須確認①.csv';

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

(async () => {
  const res = await fetch('http://localhost:3001/api/delivery/hearing-xlsx', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sheets: ['必須確認①'], info: {}, prefill: {} }),
  });
  const buf = Buffer.from(await res.arrayBuffer());
  fs.writeFileSync('_rowmatch.xlsx', buf);
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);
  const ws = wb.getWorksheet('必須確認①');

  const merges = ws.model.merges || [];
  const slave = new Set();
  for (const m of merges) {
    const [a, b] = m.split(':');
    const c2n = c => c.split('').reduce((t, ch) => t * 26 + ch.charCodeAt(0) - 64, 0);
    const r1 = parseInt(a.match(/\d+/)[0], 10);
    const c1 = c2n(a.match(/[A-Z]+/)[0]), c2 = c2n(b.match(/[A-Z]+/)[0]);
    for (let c = c1 + 1; c <= c2; c++) slave.add(`${r1}_${c}`);
  }

  const src = parseCSV(fs.readFileSync(CSV, 'utf8').replace(/^\uFEFF/, ''));
  const INTERNAL = ['のヒアリングシートへ', '非表示にして', '田中社長', '営業に確認', 'タブレットの場合不要'];

  let ng = 0;
  console.log('行| 一致 | 内容');
  for (let i = 1; i <= Math.max(src.length, ws.rowCount); i++) {
    const s = (src[i - 1] || []).map(c => c.trim())
      .filter(c => c && c !== 'TRUE' && c !== 'FALSE' && !INTERNAL.some(m => c.includes(m)))
      .join(' | ');
    const r = ws.getRow(i);
    const xs = [];
    r.eachCell({ includeEmpty: false }, (c, col) => {
      if (slave.has(`${i}_${col}`)) return;
      const v = String(c.value ?? '').trim();
      if (v && v !== '□' && v !== '✔') xs.push(v);
    });
    const x = xs.join(' | ');
    const same = s.slice(0, 24) === x.slice(0, 24);
    if (!same) ng++;
    console.log(`${String(i).padStart(2)}| ${same ? 'OK' : '≠≠'} | ${(same ? s : 'CSV:' + s.slice(0, 40) + ' ／ XLS:' + x.slice(0, 40)).slice(0, 96)}`);
  }
  console.log('\n不一致:', ng, '行 ← 0が正');
})();
