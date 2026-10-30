// 最終監査: 社内用を除いた「お客様に見せる内容」が雛形と一致するか
const fs = require('fs');
const path = require('path');
const ExcelJS = require('./node_modules/exceljs');

const DL = 'C:\\Users\\fyone\\Downloads';
const SHEETS = ['必須確認①', '必須確認②', '必須確認③', 'PMS',
  'スマートロック①', 'スマートロック②', '事前チェックイン', 'フロントチェックイン',
  'カードキー', 'シリンダー錠', 'プリンタ', 'ルームタブレット',
  '現金決済', '端末カード決済', 'PayPay決済'];

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

// 社内用ゾーンを特定（生成側と同じロジック）
function internalCols(rows) {
  const ncol = Math.max(...rows.map(r => r.length));
  const bad = new Set();
  let zone = null;
  outer: for (const r of rows.slice(0, 8)) {
    for (let c = 0; c < r.length; c++) {
      if ((r[c] || '').includes('社内用の情報欄')) { zone = c; break outer; }
    }
  }
  if (zone !== null) for (let c = zone; c < ncol; c++) bad.add(c);
  for (let c = 0; c < ncol; c++) {
    const head = rows.slice(0, 6).map(r => r[c] || '').join(' ');
    if (/DMS入力項目|クライアント|物件一覧/.test(head)) bad.add(c);
  }
  return bad;
}
const CELL_NG = /のヒアリングシートへ|田中社長|営業に確認|タブレットの場合不要/;

(async () => {
  const res = await fetch('http://localhost:3001/api/delivery/hearing-xlsx', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sheets: SHEETS, info: {}, prefill: {}, fill: {} }),
  });
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(Buffer.from(await res.arrayBuffer()));

  let ngTotal = 0;
  for (const name of SHEETS) {
    const f = fs.readdirSync(DL).find(x => x.includes(' - ' + name + '.csv'));
    if (!f) { console.log(`${name.padEnd(16)} CSVなし`); continue; }
    const src = parseCSV(fs.readFileSync(path.join(DL, f), 'utf8').replace(/^\uFEFF/, ''));
    const bad = internalCols(src);

    // 期待値: 社内用を除いたテキスト集合
    const want = new Set();
    src.forEach(r => r.forEach((v, c) => {
      const t = (v || '').trim();
      if (t && t !== 'TRUE' && t !== 'FALSE' && !bad.has(c) && !CELL_NG.test(t)) want.add(t);
    }));

    const ws = wb.getWorksheet(name);
    const got = new Set();
    ws.eachRow(r => r.eachCell({ includeEmpty: false }, c => {
      const t = String(c.value ?? '').trim();
      if (t && t !== '□' && t !== '✔') got.add(t);
    }));

    const missing = [...want].filter(x => !got.has(x));
    const extra = [...got].filter(x => !want.has(x));
    const ok = missing.length === 0 && extra.length === 0;
    if (!ok) ngTotal++;
    console.log(`${ok ? 'OK  ' : 'NG  '}${name.padEnd(16)} 期待${String(want.size).padEnd(4)} 実際${String(got.size).padEnd(4)}${ok ? '' : ` 欠落${missing.length} 余分${extra.length}`}`);
    missing.slice(0, 2).forEach(m => console.log(`      欠落: ${m.slice(0, 44)}`));
    extra.slice(0, 2).forEach(m => console.log(`      余分: ${m.slice(0, 44)}`));
  }
  console.log('\n不一致シート:', ngTotal, '← 0が正');
})();
