// 最終検証: 雛形CSVとExcel出力が一致するかを直接比較する
const fs = require('fs');
const ExcelJS = require('./node_modules/exceljs');
const path = require('path');

const DL = 'C:\\Users\\fyone\\Downloads';
const SHEETS = ['必須確認①', '必須確認②', '必須確認③', 'PMS',
  'スマートロック①', '事前チェックイン', 'カードキー', 'プリンタ',
  'シリンダー錠', 'ルームタブレット', '現金決済', '端末カード決済', 'PayPay決済'];

// 社内用列の判定（生成側と同じ）
const INTERNAL = ['のヒアリングシートへ', 'DMS入力項目', 'タブレットの場合不要',
  '社内用', '田中社長', '営業に確認', 'クライアント', '物件一覧', '非表示にして'];

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
    body: JSON.stringify({ sheets: SHEETS, info: { client: 'テスト' }, prefill: {} }),
  });
  const buf = Buffer.from(await res.arrayBuffer());
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);

  console.log('%-16s %-8s %-8s %s', 'シート', '雛形設問', 'Excel', '判定');
  let ng = 0;
  for (const name of SHEETS) {
    const f = fs.readdirSync(DL).find(x => x.includes(' - ' + name + '.csv'));
    if (!f) { console.log(`  ${name.padEnd(14)} CSVなし`); continue; }
    const rows = parseCSV(fs.readFileSync(path.join(DL, f), 'utf8').replace(/^\uFEFF/, ''));
    // 社内用列を除いた、意味のあるテキストを集合化
    const ncol = Math.max(...rows.map(r => r.length));
    const bad = new Set();
    for (let c = 0; c < ncol; c++) {
      const col = rows.map(r => r[c] || '').join(' ');
      if (INTERNAL.some(m => col.includes(m))) bad.add(c);
    }
    const srcSet = new Set();
    rows.forEach(r => r.forEach((v, c) => {
      const t = (v || '').trim();
      if (t && t !== 'TRUE' && t !== 'FALSE' && !bad.has(c)) srcSet.add(t);
    }));

    const ws = wb.getWorksheet(name);
    const xlsSet = new Set();
    ws.eachRow(r => r.eachCell({ includeEmpty: false }, c => {
      const t = String(c.value ?? '').trim();
      if (t && t !== '□' && t !== '✔') xlsSet.add(t);
    }));

    const missing = [...srcSet].filter(x => !xlsSet.has(x));
    const extra = [...xlsSet].filter(x => !srcSet.has(x));
    const ok = missing.length === 0;
    if (!ok) ng++;
    console.log(`  ${name.padEnd(14)} ${String(srcSet.size).padEnd(8)} ${String(xlsSet.size).padEnd(8)} ${ok ? 'OK' : 'NG 欠落' + missing.length}`);
    if (missing.length) missing.slice(0, 3).forEach(m => console.log(`      欠落: ${m.slice(0, 50)}`));
    if (extra.length) extra.slice(0, 2).forEach(m => console.log(`      余分: ${m.slice(0, 50)}`));
  }
  console.log('\n欠落のあるシート:', ng, '← 0が正');
})();
