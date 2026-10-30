// 「発注済み→取込→未発注」を実データで再現し、どこで消えるか特定する。
// 破壊的変更はテスト専用行にのみ行い、最後に元へ戻す。
const fs = require('fs'); const path = require('path');
const env = {};
for (const line of fs.readFileSync(path.join(__dirname, '.env.local'), 'utf8').split(/\r?\n/)) {
  const m = line.match(/^([A-Z0-9_]+)=(.*)$/); if (m) env[m[1]] = m[2].trim();
}
const URL = env.NEXT_PUBLIC_SUPABASE_URL, KEY = env.SUPABASE_SERVICE_ROLE_KEY;
const H = { apikey: KEY, Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json',
            Prefer: 'return=representation' };

const CSV_BACKED = ['P400', 'PayCube', 'VEGA3000'];
const statusKey = n => CSV_BACKED.includes(n) ? `manual_${n.toLowerCase()}_status` : `${n.toLowerCase()}_status`;

(async () => {
  // dot社の行をテスト対象にする
  const q = await fetch(`${URL}/rest/v1/delivery_items?select=id,client_name,item_key,p400_status,dashboard_todos&client_name=like.*dot*`, { headers: H });
  const rows = await q.json();
  const row = rows.find(x => x.dashboard_todos && x.dashboard_todos['manual_p400_status']) || rows[0];
  if (!row) { console.log('target not found'); return; }
  console.log('target:', row.client_name, row.id);
  console.log('item_key:', row.item_key);
  console.log('BEFORE p400_status =', JSON.stringify(row.p400_status));
  console.log('BEFORE todos.manual_p400_status =', JSON.stringify(row.dashboard_todos?.['manual_p400_status']));

  // --- import-csv と同じ upsert を item_key で実行して何が起きるか見る ---
  // ※ import-csv は dashboard_todos を送らない。onConflict=item_key。
  const payload = [{
    item_key: row.item_key,
    client_name: row.client_name,
    p400_status: '',              // CSVのP400手配状況が空欄だった場合を模擬
    last_imported_at: new Date().toISOString(),
    missing_in_last_import: false,
  }];
  const up = await fetch(`${URL}/rest/v1/delivery_items?on_conflict=item_key`, {
    method: 'POST',
    headers: { ...H, Prefer: 'resolution=merge-duplicates,return=representation' },
    body: JSON.stringify(payload),
  });
  const res = await up.json();
  if (!up.ok) { console.log('upsert failed', up.status, JSON.stringify(res).slice(0, 400)); return; }

  const after = Array.isArray(res) ? res[0] : res;
  console.log('\n--- upsert(import模擬) 後 ---');
  console.log('AFTER p400_status =', JSON.stringify(after.p400_status));
  console.log('AFTER todos =', JSON.stringify(after.dashboard_todos));
  const kept = after.dashboard_todos && after.dashboard_todos['manual_p400_status'];
  console.log('\nmanual_p400_status 保持:', kept ? `YES ("${kept}")` : 'NO (消えた!)');

  // UIの表示判定を再現
  const disp = (after.dashboard_todos || {})[statusKey('P400')] || after.p400_status || null;
  console.log('画面表示は:', disp || '未発注');
})();
