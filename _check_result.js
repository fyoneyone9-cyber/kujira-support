// 生成された工程管理表に、どの区分が残っているか確認する
const ExcelJS = require('./node_modules/exceljs');
const fs = require('fs');

const FILES = [
  'C:\\Users\\fyone\\Downloads\\工程管理_株式会社ビジョン.xlsx',
  'C:\\Users\\fyone\\Downloads\\工程管理_株式会社ビジョン (1).xlsx',
];

function txt(v) {
  if (v == null) return '';
  if (typeof v === 'object') {
    if (Array.isArray(v.richText)) return v.richText.map(r => r.text || '').join('');
    if (v.result !== undefined) return String(v.result);
    if (v.text !== undefined) return String(v.text);
    return '';
  }
  return String(v);
}

(async () => {
  for (const f of FILES) {
    if (!fs.existsSync(f)) { console.log('なし:', f); continue; }
    const wb = new ExcelJS.Workbook();
    await wb.xlsx.readFile(f);
    const ws = wb.worksheets.find(w => w.name.includes('工程')) || wb.worksheets[0];
    console.log(`\n===== ${f.split('\\').pop()} =====`);
    console.log(`シート: ${ws.name} / 行数: ${ws.rowCount}`);

    const cnt = {};
    ws.eachRow((r, i) => {
      if (i <= 3) return;
      const c = txt(r.getCell(3).value).trim();   // C列=区分
      if (!c) return;
      cnt[c] = (cnt[c] || 0) + 1;
    });
    console.log('残っている区分:');
    Object.entries(cnt).sort().forEach(([k, v]) => console.log(`   ${k.padEnd(24)} ${v}行`));
  }
})();
