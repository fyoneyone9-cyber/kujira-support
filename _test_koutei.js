// 工程管理表: 機材構成に応じて行が削られるか検証する
const fs = require('fs');
const ExcelJS = require('./node_modules/exceljs');

async function gen(name, flags) {
  const res = await fetch('http://localhost:3001/api/delivery/koutei-xlsx', {
    method: 'POST', headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      info: { client: '株式会社ビジョン', property: 'グランピングリゾートAwaji', due: '2026-12-01' },
      flags,
    }),
  });
  const buf = Buffer.from(await res.arrayBuffer());
  const wb = new ExcelJS.Workbook();
  await wb.xlsx.load(buf);
  const ws = wb.getWorksheet('工程管理');
  const cats = new Set();
  ws.eachRow((r, i) => {
    if (i <= 3) return;
    const c = String(r.getCell(3).value ?? '').trim();
    if (c) cats.add(c);
  });
  console.log(`\n■ ${name}`);
  console.log(`  status=${res.status} 残=${res.headers.get('X-Rows-Kept')} 削除=${res.headers.get('X-Rows-Removed')} 総行=${ws.rowCount}`);
  console.log(`  残った区分: ${[...cats].sort().join(' / ')}`);
  return { ws, buf };
}

(async () => {
  // ケース1: ビジョン社（PMS + スマートロック + パスポートリーダー + Surface）
  const a = await gen('ビジョン社の実構成', {
    pms: true, smartlock: true, passport: true, surface: true,
    cardkey: false, keybox: false, kiosk: false, kiosk_desk: false,
    roomtablet: false, tablet: false, p400: false, paycube: false,
    paypay: false, sumaho: false, hojokin: false,
  });

  // ケース2: 全部あり
  await gen('全機材あり', {
    pms: true, smartlock: true, passport: true, surface: true,
    cardkey: true, keybox: true, kiosk: true, kiosk_desk: true,
    roomtablet: true, tablet: true, p400: true, paycube: true,
    paypay: true, sumaho: true, hojokin: true,
  });

  // ケース3: 最小（共通のみ）
  await gen('機材なし（共通のみ）', {});

  fs.writeFileSync('_koutei_test.xlsx', a.buf);
  console.log('\n--- ビジョン社 先頭8行 ---');
  a.ws.eachRow((r, i) => {
    if (i > 8) return;
    const v = [1, 2, 3, 4].map(c => String(r.getCell(c).value ?? '').replace(/\n/g, ' ').slice(0, 22));
    console.log(`  ${String(i).padStart(2)}| ${v.join(' | ')}`);
  });
})();
