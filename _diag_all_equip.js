// 「発注済みがリセットされた」の実体を特定する。
// UIの表示ロジックを再現し、どの行が何を表示するはずかを出す。
const fs = require('fs'); const path = require('path');
const env = {};
for (const line of fs.readFileSync(path.join(__dirname, '.env.local'), 'utf8').split(/\r?\n/)) {
  const m = line.match(/^([A-Z0-9_]+)=(.*)$/); if (m) env[m[1]] = m[2].trim();
}
const URL = env.NEXT_PUBLIC_SUPABASE_URL, KEY = env.SUPABASE_SERVICE_ROLE_KEY;
const H = { apikey: KEY, Authorization: `Bearer ${KEY}` };

const CSV_BACKED = ['P400', 'PayCube', 'VEGA3000'];
const statusKey = n => n === 'キーボックス' ? 'keybox_status'
  : CSV_BACKED.includes(n) ? `manual_${n.toLowerCase()}_status`
  : `${n.toLowerCase()}_status`;

(async () => {
  const r = await fetch(`${URL}/rest/v1/delivery_items?select=client_name,product_name,status,equipment,p400_status,paycube_status,vega3000_status,dashboard_todos&limit=2000`, { headers: H });
  const rows = await r.json();

  const getStatus = (it, name) => {
    const manual = (it.dashboard_todos || {})[statusKey(name)] || null;
    if (manual) return manual;
    if (name === 'P400') return it.p400_status || null;
    if (name === 'PayCube') return it.paycube_status || null;
    if (name === 'VEGA3000') return it.vega3000_status || null;
    return null;
  };

  // P400を持つ案件（UIで「P400 x N」が出る行）
  const hasP400 = rows.filter(x => (x.equipment || []).some(e => e.name === 'P400'));
  console.log('P400を持つ案件:', hasP400.length, '/', rows.length);

  let shown = 0, unordered = 0;
  for (const x of hasP400) {
    const st = getStatus(x, 'P400');
    if (!st) unordered++;
    if (shown < 25) {
      const eq = (x.equipment || []).find(e => e.name === 'P400');
      console.log(`  ${(x.client_name || '').slice(0, 22).padEnd(22)} x${eq?.value || '?'}  表示="${st || '未発注'}"  csv=${JSON.stringify(x.p400_status)}  todos.manual=${JSON.stringify((x.dashboard_todos || {})['manual_p400_status'])}`);
      shown++;
    }
  }
  console.log(`\n「未発注」と表示される行: ${unordered} / ${hasP400.length}`);

  // 旧キー(p400_status)が dashboard_todos に入っている行 = V2移行前の手動値の可能性
  const oldKey = rows.filter(x => x.dashboard_todos && x.dashboard_todos['p400_status']);
  console.log(`\ndashboard_todos に旧キー 'p400_status' を持つ行: ${oldKey.length}`);
  for (const x of oldKey.slice(0, 20)) {
    console.log('   ', x.client_name, '->', JSON.stringify(x.dashboard_todos['p400_status']));
  }
})();
