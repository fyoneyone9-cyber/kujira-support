// 既存データ同期の「リスク判定」（読み取りのみ）
//   発注ブロック解除条件は page.tsx L1103付近:
//     ps !== '入金確認済み' && ps !== '入金不要（無償）' なら発注系ステータス禁止
//   → この2値以外を同期しても発注可否は変わらない = 無害
const fs = require('fs'); const path = require('path');
const env = {};
for (const line of fs.readFileSync(path.join(__dirname, '.env.local'), 'utf8').split(/\r?\n/)) {
  const m = line.match(/^([A-Z0-9_]+)=(.*)$/); if (m) env[m[1]] = m[2].trim();
}
const URL = env.NEXT_PUBLIC_SUPABASE_URL, KEY = env.SUPABASE_SERVICE_ROLE_KEY;
const H = { apikey: KEY, Authorization: `Bearer ${KEY}` };
const UNLOCK = ['入金確認済み', '入金不要（無償）'];

const SHARED = k =>
  /^manual_.*_status$/.test(k) || /_order_date$/.test(k) ||
  /_arrive_date$/.test(k) || /_actual_date$/.test(k) ||
  k === 'keybox_status' || k === 'paypay_status' ||
  k === 'payment_status' || k === 'payment_memo';

(async () => {
  const r = await fetch(`${URL}/rest/v1/delivery_items?select=id,client_name,install_address,product_name,status,equipment,locked,dashboard_todos&limit=2000`, { headers: H });
  const rows = await r.json();
  const g = new Map();
  for (const x of rows) {
    const k = `${x.client_name}\u0001${x.install_address || ''}`;
    if (!g.has(k)) g.set(k, []);
    g.get(k).push(x);
  }

  const safe = [], risky = [];
  for (const [key, v] of g) {
    if (v.length < 2) continue;
    const keys = new Set();
    for (const x of v) for (const k of Object.keys(x.dashboard_todos || {})) if (SHARED(k)) keys.add(k);
    for (const k of keys) {
      const vals = [...new Set(v.map(x => (x.dashboard_todos || {})[k]).filter(z => z != null && z !== ''))];
      if (vals.length !== 1) continue;
      const val = vals[0];
      for (const x of v) {
        if (x.locked) continue;
        const cur = (x.dashboard_todos || {})[k];
        if (cur != null && cur !== '') continue;
        const unlocks = (k === 'payment_status') && UNLOCK.includes(val);
        const eq = (x.equipment || []).map(e => e.name);
        const gated = eq.filter(n => n === 'PayCube' || n === 'キーボックス');
        const rec = { c: x.client_name, p: (x.product_name || '').slice(0, 22), k, val, gated, st: x.status };
        (unlocks && gated.length ? risky : safe).push(rec);
      }
    }
  }
  const show = (t, a) => {
    console.log(`\n=== ${t} : ${a.length}件 ===`);
    for (const x of a) console.log(`  ${x.c} / ${x.p} [${x.st}]  ${x.k} = ${JSON.stringify(x.val)}${x.gated.length ? '  ⚠発注ゲート対象: ' + x.gated.join(',') : ''}`);
  };
  show('無害（発注可否は変わらない）', safe);
  show('要確認（発注ブロックが解除される）', risky);
})();
