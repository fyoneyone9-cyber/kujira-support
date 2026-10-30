// 「発注済み」がリセットされた件の実データ診断
const fs = require('fs'); const path = require('path');
const env = {};
for (const line of fs.readFileSync(path.join(__dirname, '.env.local'), 'utf8').split(/\r?\n/)) {
  const m = line.match(/^([A-Z0-9_]+)=(.*)$/); if (m) env[m[1]] = m[2].trim();
}
const URL = env.NEXT_PUBLIC_SUPABASE_URL, KEY = env.SUPABASE_SERVICE_ROLE_KEY;
const H = { apikey: KEY, Authorization: `Bearer ${KEY}` };

(async () => {
  const r = await fetch(`${URL}/rest/v1/delivery_items?select=id,client_name,product_name,p400_status,paycube_status,vega3000_status,dashboard_todos,last_imported_at,missing_in_last_import&limit=2000`, { headers: H });
  const rows = await r.json();
  console.log('total rows:', rows.length);

  // 1) manual_* を保持している行
  const withManual = rows.filter(x => x.dashboard_todos &&
    Object.keys(x.dashboard_todos).some(k => k.startsWith('manual_')));
  console.log('\n[1] manual_* を持つ行:', withManual.length);
  for (const x of withManual.slice(0, 20)) {
    const picked = Object.fromEntries(Object.entries(x.dashboard_todos).filter(([k]) => k.startsWith('manual_')));
    console.log('   ', x.client_name, JSON.stringify(picked), '| csv.p400=', JSON.stringify(x.p400_status));
  }

  // 2) 直近インポート時刻
  const times = [...new Set(rows.map(x => x.last_imported_at).filter(Boolean))].sort();
  console.log('\n[2] last_imported_at (最新5):');
  times.slice(-5).forEach(t => console.log('   ', t));

  // 3) dot社の全行
  console.log('\n[3] 株式会社dot の全行:');
  for (const x of rows.filter(x => (x.client_name || '').includes('dot'))) {
    console.log('   id=', x.id);
    console.log('     product=', x.product_name);
    console.log('     p400_status=', JSON.stringify(x.p400_status));
    console.log('     todos=', JSON.stringify(x.dashboard_todos));
    console.log('     imported=', x.last_imported_at, 'missing=', x.missing_in_last_import);
  }
})();
