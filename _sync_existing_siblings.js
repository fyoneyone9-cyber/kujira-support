// [SIBLING_SYNC_V1] 既存データの穴埋め。
//   同一現場(会社名+設置先住所)の兄弟行で、共通項目が「片方にだけ入っている」ものを揃える。
//   ・空の行にだけ補完する(既に値がある行は上書きしない = 非破壊)
//   ・値が食い違っている場合は触らず警告のみ(どちらが正しいか機械judgeできないため)
//   DRY=1 で変更内容の確認のみ。
const fs = require('fs'); const path = require('path');
const env = {};
for (const line of fs.readFileSync(path.join(__dirname, '.env.local'), 'utf8').split(/\r?\n/)) {
  const m = line.match(/^([A-Z0-9_]+)=(.*)$/); if (m) env[m[1]] = m[2].trim();
}
const URL = env.NEXT_PUBLIC_SUPABASE_URL, KEY = env.SUPABASE_SERVICE_ROLE_KEY;
const H = { apikey: KEY, Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' };
const DRY = process.env.DRY === '1';

const SHARED = k =>
  /^manual_.*_status$/.test(k) || /_order_date$/.test(k) ||
  /_arrive_date$/.test(k) || /_actual_date$/.test(k) ||
  k === 'keybox_status' || k === 'paypay_status' ||
  k === 'payment_status' || k === 'payment_memo';

(async () => {
  const r = await fetch(`${URL}/rest/v1/delivery_items?select=id,client_name,install_address,product_name,locked,dashboard_todos&limit=2000`, { headers: H });
  const rows = await r.json();

  const g = new Map();
  for (const x of rows) {
    const k = `${x.client_name}\u0001${x.install_address || ''}`;
    if (!g.has(k)) g.set(k, []);
    g.get(k).push(x);
  }

  let changed = 0, conflicts = 0;
  for (const [key, v] of g) {
    if (v.length < 2) continue;
    // このグループで使われている共通キーを集める
    const keys = new Set();
    for (const x of v) for (const k of Object.keys(x.dashboard_todos || {})) if (SHARED(k)) keys.add(k);

    for (const k of keys) {
      const vals = [...new Set(v.map(x => (x.dashboard_todos || {})[k]).filter(z => z != null && z !== ''))];
      if (vals.length === 0) continue;
      if (vals.length > 1) {
        conflicts++;
        console.log(`! 不一致のため手動確認: ${key.split('\u0001')[0]} / ${k} -> ${JSON.stringify(vals)}`);
        continue;
      }
      const val = vals[0];
      for (const x of v) {
        if (x.locked) continue;
        const cur = (x.dashboard_todos || {})[k];
        if (cur != null && cur !== '') continue;   // 既に値がある行は触らない
        changed++;
        console.log(`${DRY ? '[DRY] ' : ''}${x.client_name} / ${(x.product_name || '').slice(0, 20)} : ${k} = ${JSON.stringify(val)}`);
        if (!DRY) {
          const body = { dashboard_todos: { ...(x.dashboard_todos || {}), [k]: val } };
          const u = await fetch(`${URL}/rest/v1/delivery_items?id=eq.${x.id}`, { method: 'PATCH', headers: H, body: JSON.stringify(body) });
          if (!u.ok) console.error('  failed', u.status, await u.text());
          else x.dashboard_todos = body.dashboard_todos;
        }
      }
    }
  }
  console.log(`\n${DRY ? 'would update' : 'updated'}: ${changed} 箇所 / 不一致スキップ: ${conflicts}`);
})();
