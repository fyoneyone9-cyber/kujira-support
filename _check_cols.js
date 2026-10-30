// [MANUAL_EQUIP_STATUS_V1] 対象カラムの有無を確認する
const fs = require('fs');
const path = require('path');
const env = {};
for (const line of fs.readFileSync(path.join(__dirname, '.env.local'), 'utf8').split(/\r?\n/)) {
  const m = line.match(/^([A-Z0-9_]+)=(.*)$/);
  if (m) env[m[1]] = m[2].trim();
}
const URL = env.NEXT_PUBLIC_SUPABASE_URL;
const KEY = env.SUPABASE_SERVICE_ROLE_KEY;

const COLS = ['p400_status', 'p400_status_manual', 'paycube_status',
  'paycube_status_manual', 'vega3000_status', 'vega3000_status_manual'];

(async () => {
  for (const c of COLS) {
    const r = await fetch(`${URL}/rest/v1/delivery_items?select=${c}&limit=1`, {
      headers: { apikey: KEY, Authorization: `Bearer ${KEY}` },
    });
    console.log(`${r.ok ? 'EXISTS ' : 'MISSING'}  ${c}`);
  }
})();
