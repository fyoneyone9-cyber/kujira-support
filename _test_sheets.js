// 株式会社ビジョンで必要シート判定を再現（読み取りのみ）
const fs = require('fs'); const path = require('path');
const env = {};
for (const line of fs.readFileSync(path.join(__dirname, '.env.local'), 'utf8').split(/\r?\n/)) {
  const m = line.match(/^([A-Z0-9_]+)=(.*)$/); if (m) env[m[1]] = m[2].trim();
}
const URL = env.NEXT_PUBLIC_SUPABASE_URL, KEY = env.SUPABASE_SERVICE_ROLE_KEY;
const H = { apikey: KEY, Authorization: `Bearer ${KEY}` };

const LOCK = /スマートロック|smart.?lock|remotelock|ttlock|epic|bitlock|qrio|akerun|igloohome|lock/i;
const CARD = /カードキー|card.?key/i;
const CYLI = /シリンダー|cylinder/i;
const PMS = /pms|airhost|suitebook|temairazu|innkeeper|staypro|宿泊|ホテル管理/i;
const TABLET = /ルームタブレット|room.?tablet/i;
const PRINTER = /プリンタ|printer/i;

(async () => {
  const r = await fetch(`${URL}/rest/v1/delivery_items?select=client_name,install_address,product_name,contact_name,equipment&client_name=like.*ビジョン*`, { headers: H });
  const rows = await r.json();
  for (const it of rows) {
    const equip = it.equipment || [];
    const t = p => equip.some(e => p.test(e.name || '') || p.test(e.value || ''));
    const sheets = [
      ['必須確認①', '全物件必須'], ['必須確認②', '全物件必須（基本情報）'], ['必須確認③', '全物件必須（部屋情報）'],
      ...(t(PMS) ? [['PMS', 'PMS連携あり']] : []),
      ...(t(LOCK) ? [['スマートロック①', 'あり'], ['スマートロック②', 'あり'], ['スマートロック③', 'あり']] : []),
      ...(t(CARD) ? [['カードキー', 'あり']] : []),
      ...(t(CYLI) ? [['シリンダー錠', 'あり']] : []),
      ...(t(/p400/i) ? [['端末カード決済', 'P400あり']] : []),
      ...(t(/paycube|pay.?cube/i) ? [['現金決済', 'PayCubeあり']] : []),
      ...(t(/paypay|pay.?pay/i) ? [['スマホカード決済', 'PayPayあり']] : []),
      ...(t(TABLET) ? [['ルームタブレット', 'あり']] : []),
      ...(t(PRINTER) ? [['プリンタ', 'あり']] : []),
      ['事前チェックイン', '全物件推奨'], ['フロントチェックイン', '有人対応がある場合'],
      ['デイユース', '日帰り利用がある場合（要確認）'],
      ['工事', 'LAN・電源が設置不可の場合（要確認）'],
      ['IT導入補助金', '補助金を利用する場合（要確認）'],
    ];
    console.log(`\n■ ${it.client_name} / ${it.product_name}`);
    console.log('  機材:', equip.map(e => [e.name, e.value].filter(Boolean).join(' ')).join('、') || '(なし)');
    console.log(`  → 必要シート ${sheets.length}枚:`);
    sheets.forEach((x, i) => console.log(`     ${i + 1}. ${x[0]}  (${x[1]})`));
  }
})();
