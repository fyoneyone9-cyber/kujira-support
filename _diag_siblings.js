// 同一顧客で複数行になっている案件の実態を調べる（読み取りのみ）
const fs = require('fs'); const path = require('path');
const env = {};
for (const line of fs.readFileSync(path.join(__dirname, '.env.local'), 'utf8').split(/\r?\n/)) {
  const m = line.match(/^([A-Z0-9_]+)=(.*)$/); if (m) env[m[1]] = m[2].trim();
}
const URL = env.NEXT_PUBLIC_SUPABASE_URL, KEY = env.SUPABASE_SERVICE_ROLE_KEY;
const H = { apikey: KEY, Authorization: `Bearer ${KEY}` };

(async () => {
  const r = await fetch(`${URL}/rest/v1/delivery_items?select=id,client_name,install_address,product_name,status,missing_in_last_import,p400_status,dashboard_todos&limit=2000`, { headers: H });
  const rows = await r.json();

  // 会社名+住所 でグルーピング（item_keyは製品名まで含むので別行になる）
  const byCA = new Map();
  for (const x of rows) {
    const k = `${x.client_name}\u0001${x.install_address || ''}`;
    if (!byCA.has(k)) byCA.set(k, []);
    byCA.get(k).push(x);
  }
  const multi = [...byCA.entries()].filter(([, v]) => v.length > 1);
  console.log(`総行数 ${rows.length} / グループ(会社+住所) ${byCA.size} / 複数行グループ ${multi.length}`);

  // 会社名のみ でもグルーピング
  const byC = new Map();
  for (const x of rows) {
    const k = x.client_name;
    if (!byC.has(k)) byC.set(k, []);
    byC.get(k).push(x);
  }
  const multiC = [...byC.entries()].filter(([, v]) => v.length > 1);
  console.log(`グループ(会社名のみ) ${byC.size} / 複数行 ${multiC.length}`);

  console.log('\n--- 会社+住所 が同じで複数行 (上位12) ---');
  for (const [k, v] of multi.slice(0, 12)) {
    const [c, a] = k.split('\u0001');
    console.log(`\n■ ${c} / ${(a || '(住所なし)').slice(0, 30)}  -> ${v.length}行`);
    for (const x of v) {
      const t = x.dashboard_todos || {};
      const keys = Object.keys(t).filter(kk => /^manual_|_order_date$|_arrive_date$|_status$/.test(kk));
      console.log(`   - ${(x.product_name || '').slice(0, 26).padEnd(26)} status=${x.status} missing=${x.missing_in_last_import} p400=${JSON.stringify(x.p400_status)}`);
      console.log(`     todos: ${keys.length ? keys.map(kk => `${kk}=${JSON.stringify(t[kk])}`).join(' , ') : '(なし)'}`);
    }
  }

  // 「片方だけ値が入っている」グループ = 同期したいケース
  let需要 = 0;
  for (const [, v] of multi) {
    const has = v.filter(x => {
      const t = x.dashboard_todos || {};
      return Object.keys(t).some(kk => kk.startsWith('manual_') || /_order_date$|_arrive_date$/.test(kk)) || (x.p400_status || '').trim();
    });
    if (has.length > 0 && has.length < v.length) 需要++;
  }
  console.log(`\n片方だけ入力済みのグループ(同期したいケース): ${需要}`);
})();
