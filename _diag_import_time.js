// 「最終取込 10/27」表示と実データの食い違いを調べる（読み取りのみ）
const fs = require('fs'); const path = require('path');
const env = {};
for (const line of fs.readFileSync(path.join(__dirname, '.env.local'), 'utf8').split(/\r?\n/)) {
  const m = line.match(/^([A-Z0-9_]+)=(.*)$/); if (m) env[m[1]] = m[2].trim();
}
const URL = env.NEXT_PUBLIC_SUPABASE_URL, KEY = env.SUPABASE_SERVICE_ROLE_KEY;
const H = { apikey: KEY, Authorization: `Bearer ${KEY}` };

(async () => {
  const r = await fetch(`${URL}/rest/v1/delivery_items?select=id,client_name,last_imported_at,missing_in_last_import,updated_at&limit=2000`, { headers: H });
  const rows = await r.json();
  console.log('total rows:', rows.length);

  const times = rows.map(x => x.last_imported_at).filter(Boolean).sort();
  console.log('\n[last_imported_at]');
  console.log('  最古:', times[0]);
  console.log('  最新:', times[times.length - 1]);

  // 日付ごとの件数
  const byDay = {};
  for (const t of times) { const d = t.slice(0, 10); byDay[d] = (byDay[d] || 0) + 1; }
  console.log('\n  日付別件数:');
  Object.keys(byDay).sort().forEach(d => console.log('   ', d, byDay[d]));

  const nullT = rows.filter(x => !x.last_imported_at).length;
  console.log('\n  last_imported_at が null:', nullT);

  const missing = rows.filter(x => x.missing_in_last_import).length;
  console.log('  missing_in_last_import=true:', missing);

  // updated_at があるか
  if (rows[0] && 'updated_at' in rows[0]) {
    const u = rows.map(x => x.updated_at).filter(Boolean).sort();
    console.log('\n[updated_at] 最新:', u[u.length - 1]);
  }
})();
