// PayPayを持つ案件があるか確認する
const fs = require('fs');
const env = fs.readFileSync('.env.local', 'utf8');
const url = (env.match(/NEXT_PUBLIC_SUPABASE_URL=(.+)/) || [])[1].trim();
const key = (env.match(/SUPABASE_SERVICE_ROLE_KEY=(.+)/) || [])[1].trim();

(async () => {
  const r = await fetch(`${url}/rest/v1/delivery_items?select=client_name,equipment&limit=500`,
    { headers: { apikey: key, Authorization: `Bearer ${key}` } });
  const rows = await r.json();
  const hit = rows.filter(it =>
    (it.equipment || []).some(e => /paypay/i.test((e.name || '') + (e.value || ''))));
  console.log(`全${rows.length}件中、PayPayを持つ案件: ${hit.length}件`);
  hit.slice(0, 8).forEach(it =>
    console.log(`  ${it.client_name}: ${(it.equipment || []).map(e => e.name).join(', ')}`));

  // 機材名の一覧（どんな名前で入っているか）
  const names = new Set();
  rows.forEach(it => (it.equipment || []).forEach(e => names.add(e.name)));
  console.log('\n=== 機材名の種類 ===');
  [...names].sort().forEach(n => console.log('  ' + n));
})();
