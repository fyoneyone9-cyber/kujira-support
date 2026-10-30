// 新しい fillInfo が全シートで何箇所入力するかシミュレートする
const fs = require('fs');
const defs = JSON.parse(
  fs.readFileSync('src/lib/hearingSheetDefs.ts', 'utf8').split('= ')[1].trim()
);

const p = {
  client: '株式会社ビジョン',
  contact: '石川様',
  property: '〒656-2401 兵庫県淡路市岩屋2604',
  tel: '0799-00-0000',
  email: 'ishikawa@vision.co.jp',
  rooms: '20',
  pms: 'suitebook',
  cardkeyMaker: 'MIWA',
  lockMaker: 'EPIC',
};

let zip = '', addr = p.property || '';
const m = addr.match(/〒?\s*(\d{3}-?\d{4})/);
if (m) { zip = m[1]; addr = addr.replace(m[0], '').trim(); }

const PLAN = {
  '必須確認②': [
    ['組織名', p.client],
    ['メールアドレス（代表）', p.email],
    ['お電話番号（代表）', p.tel],
    ['DMSにログインされる方のお名前', p.contact],
    ['DMSにログインされる方のメールアドレス', p.email],
    ['物件名', p.propertyName || addr],
    ['物件の住所', addr],
    ['物件の郵便番号', zip],
    ['領収書に印字する電話番号', p.tel],
    ['緊急連絡先電話番号', p.tel],
    ['物件内にあるお部屋の総数', p.rooms],
  ],
  '必須確認③': [['お部屋の総数', p.rooms]],
  'PMS': [['PMSの名称', p.pms], ['ご利用のPMS', p.pms]],
  'カードキー': [
    ['メーカーをご回答', p.cardkeyMaker],
    ['お名前', p.contact],
    ['携帯電話番号', p.tel],
    ['メールアドレス', p.email],
  ],
  'PayPay決済': [['お名前', p.contact], ['メールアドレス', p.email]],
  'スマートロック①': [['メーカー', p.lockMaker]],
};

let total = 0;
for (const sheetName of Object.keys(PLAN)) {
  const rows = defs[sheetName];
  if (!rows) { console.log(`${sheetName}: シートなし`); continue; }
  let ansCol = 0;
  for (let r = 0; r < Math.min(6, rows.length); r++) {
    for (let c = 0; c < rows[r].length; c++) {
      if (String(rows[r][c]).indexOf('ご回答欄') >= 0) { ansCol = c + 1; break; }
    }
    if (ansCol) break;
  }
  if (!ansCol) { console.log(`${sheetName}: 回答欄なし → スキップ`); continue; }

  console.log(`\n=== ${sheetName} (回答欄=${ansCol}列) ===`);
  const used = {};
  let n = 0;
  for (const [key, val] of PLAN[sheetName]) {
    if (!val) continue;
    let hit = false;
    for (let r2 = 0; r2 < rows.length; r2++) {
      if (used[r2]) continue;
      if (rows[r2].join(' ').indexOf(key) < 0) continue;
      console.log(`  ✅ 行${r2 + 1}  ${key} = ${val}`);
      used[r2] = true; n++; hit = true;
      break;
    }
    if (!hit) console.log(`  ×  ${key}（該当行なし）`);
  }
  total += n;
}
console.log('\n合計 自動入力:', total, '箇所');
