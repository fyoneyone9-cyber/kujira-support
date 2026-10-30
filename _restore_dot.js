// 先ほどの upsert 模擬テストで p400_status を "発注済み" -> "" に変えてしまったので戻す。
const fs = require('fs'); const path = require('path');
const env = {};
for (const line of fs.readFileSync(path.join(__dirname, '.env.local'), 'utf8').split(/\r?\n/)) {
  const m = line.match(/^([A-Z0-9_]+)=(.*)$/); if (m) env[m[1]] = m[2].trim();
}
const URL = env.NEXT_PUBLIC_SUPABASE_URL, KEY = env.SUPABASE_SERVICE_ROLE_KEY;
const H = { apikey: KEY, Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json',
            Prefer: 'return=representation' };
const ID = '42febed7-34ee-4a3a-a6a0-c4721b73bead';

(async () => {
  const r = await fetch(`${URL}/rest/v1/delivery_items?id=eq.${ID}`, {
    method: 'PATCH', headers: H,
    body: JSON.stringify({ p400_status: '発注済み' }),
  });
  const j = await r.json();
  const row = Array.isArray(j) ? j[0] : j;
  console.log('restored p400_status =', JSON.stringify(row.p400_status));
  console.log('manual_p400_status  =', JSON.stringify(row.dashboard_todos?.['manual_p400_status']));
})();
