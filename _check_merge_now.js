// なぜ結合が0件なのかを調べる
const fs = require('fs');
const ExcelJS = require('./node_modules/exceljs');

(async () => {
  const res = await fetch('http://localhost:3001/api/delivery/hearing-xlsx', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ sheets: ['必須確認①'], info: {}, prefill: {} }),
  });
  const buf = Buffer.from(await res.arrayBuffer());
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);
  const ws = wb.getWorksheet('必須確認①');

  console.log('model.merges:', JSON.stringify(ws.model.merges || []));
  console.log('_merges keys:', Object.keys(ws._merges || {}).length);

  // 定義側に「同じ文字列が複数列に入っている行」があるか
  const defs = JSON.parse(
    fs.readFileSync('src/lib/hearingSheetDefs.ts', 'utf8').split('= ')[1].trim()
  );
  const d = defs['必須確認①'];
  console.log('\n--- 定義側: 同一文字列が複数列にある行 ---');
  let n = 0;
  d.forEach((row, i) => {
    const vals = row.filter(x => x);
    const uniq = new Set(vals);
    if (vals.length > 1 && uniq.size < vals.length) {
      console.log(`  行${i}: ${JSON.stringify(row).slice(0, 110)}`);
      n++;
    }
  });
  console.log(`  -> ${n}行（0なら結合対象が元々ない＝CSVが既に1セルのみ）`);

  console.log('\n--- 定義側 先頭6行の実体 ---');
  d.slice(0, 6).forEach((r, i) => console.log(`  ${i}: ${JSON.stringify(r).slice(0, 130)}`));
})();
