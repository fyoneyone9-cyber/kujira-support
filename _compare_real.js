// ユーザーがDLした実物と雛形CSVを、行ごとに並べて比較する
const fs = require('fs');
const path = require('path');
const ExcelJS = require('./node_modules/exceljs');

const XLSX = 'C:\\Users\\fyone\\Downloads\\ヒアリングシート_株式会社ビジョン (3).xlsx';
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
  if (!fs.existsSync(XLSX)) { console.log('xlsx not found:', XLSX); return; }
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.readFile(XLSX);
  console.log('=== シート一覧 ===');
  wb.eachSheet(ws => console.log(`  ${ws.name}  rows=${ws.rowCount} cols=${ws.columnCount}`));

  const ws = wb.getWorksheet('必須確認①');
  if (!ws) { console.log('必須確認①なし'); return; }

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

  console.log('\n=== 行ごとの比較（左=雛形CSV / 右=生成xlsx）===');
  const n = Math.max(src.length, ws.rowCount);
  for (let i = 1; i <= Math.min(n, 34); i++) {
    const s = (src[i - 1] || []).map(c => c.trim()).filter(Boolean).join(' | ').slice(0, 62);
    const r = ws.getRow(i);
    const xs = [];
    r.eachCell({ includeEmpty: false }, (c, col) => {
      if (slave.has(`${i}_${col}`)) return;
      const v = String(c.value ?? '').trim().replace(/\n/g, ' ');
      if (v) xs.push(v);
    });
    const x = xs.join(' | ').slice(0, 62);
    const mark = (s.slice(0, 20) === x.slice(0, 20)) ? '  ' : '≠≠';
    console.log(`${String(i).padStart(2)}${mark}CSV[${s}]`);
    console.log(`     XLS[${x}]`);
  }
})();
