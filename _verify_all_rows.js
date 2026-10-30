// 全シートを雛形CSVと行単位で突き合わせる
const fs = require('fs');
const path = require('path');
const ExcelJS = require('./node_modules/exceljs');

const DL = 'C:\\Users\\fyone\\Downloads';
const SHEETS = ['必須確認①', '必須確認②', '必須確認③', 'PMS',
  'スマートロック①', 'スマートロック②', '事前チェックイン', 'フロントチェックイン',
  'カードキー', 'シリンダー錠', 'プリンタ', 'ルームタブレット',
  '現金決済', '端末カード決済', 'PayPay決済'];
const INTERNAL = ['のヒアリングシートへ', '非表示にして', '田中社長', '営業に確認',
  'タブレットの場合不要', 'DMS入力項目', 'クライアント', '物件一覧'];

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
const norm = s => s.replace(/\s+/g, '').slice(0, 20);

(async () => {
  const res = await fetch('http://localhost:3001/api/delivery/hearing-xlsx', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sheets: SHEETS, info: {}, prefill: {}, fill: {} }),
  });
  const buf = Buffer.from(await res.arrayBuffer());
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);

  let totalNG = 0;
  for (const name of SHEETS) {
    const f = fs.readdirSync(DL).find(x => x.includes(' - ' + name + '.csv') || x.includes(' - ' + name + '（'));
    if (!f) { console.log(`${name.padEnd(16)} CSVなし`); continue; }
    const src = parseCSV(fs.readFileSync(path.join(DL, f), 'utf8').replace(/^\uFEFF/, ''));
    const ws = wb.getWorksheet(name);
    if (!ws) { console.log(`${name.padEnd(16)} シートなし`); totalNG++; continue; }

    const merges = ws.model.merges || [];
    const slave = new Set();
    for (const m of merges) {
      const [a, b] = m.split(':');
      const c2n = c => c.split('').reduce((t, ch) => t * 26 + ch.charCodeAt(0) - 64, 0);
      const r1 = parseInt(a.match(/\d+/)[0], 10);
      const c1 = c2n(a.match(/[A-Z]+/)[0]), c2 = c2n(b.match(/[A-Z]+/)[0]);
      for (let c = c1 + 1; c <= c2; c++) slave.add(`${r1}_${c}`);
    }

    let ng = 0; const samples = [];
    const n = Math.max(src.length, ws.rowCount);
    for (let i = 1; i <= n; i++) {
      const s = (src[i - 1] || []).map(c => c.trim())
        .filter(c => c && c !== 'TRUE' && c !== 'FALSE' && !INTERNAL.some(m => c.includes(m)));
      const r = ws.getRow(i);
      const xs = [];
      r.eachCell({ includeEmpty: false }, (c, col) => {
        if (slave.has(`${i}_${col}`)) return;
        const v = String(c.value ?? '').trim();
        if (v && v !== '□' && v !== '✔') xs.push(v);
      });
      const a = norm(s.join('')), b = norm(xs.join(''));
      if (a !== b) {
        ng++;
        if (samples.length < 2) samples.push(`  行${i}: CSV[${s.join('|').slice(0, 36)}] XLS[${xs.join('|').slice(0, 36)}]`);
      }
    }
    totalNG += ng;
    console.log(`${name.padEnd(16)} CSV=${String(src.length).padEnd(4)} XLS=${String(ws.rowCount).padEnd(4)} ズレ=${ng}`);
    samples.forEach(x => console.log(x));
  }
  console.log('\n総ズレ数:', totalNG);
})();
