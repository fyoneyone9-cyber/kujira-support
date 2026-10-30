// 同一「会社名+住所」で複数行になっている案件の統計（読み取りのみ）
const fs = require('fs'); const path = require('path');
const env = {};
for (const line of fs.readFileSync(path.join(__dirname, '.env.local'), 'utf8').split(/\r?\n/)) {
  const m = line.match(/^([A-Z0-9_]+)=(.*)$/); if (m) env[m[1]] = m[2].trim();
}
const URL = env.NEXT_PUBLIC_SUPABASE_URL, KEY = env.SUPABASE_SERVICE_ROLE_KEY;
const H = { apikey: KEY, Authorization: `Bearer ${KEY}` };

const SHARED_RE = /^(manual_.*_status|.*_order_date|.*_arrive_date|.*_actual_date|keybox_status|paypay_status|payment_status|payment_memo)$/;

(async () => {
  const r = await fetch(`${URL}/rest/v1/delivery_items?select=id,client_name,install_address,product_name,status,missing_in_last_import,p400_status,paycube_status,vega3000_status,dashboard_todos&limit=2000`, { headers: H });
  const rows = await r.json();

  const byCA = new Map();
  for (const x of rows) {
    const k = `${x.client_name}\u0001${x.install_address || ''}`;
    if (!byCA.has(k)) byCA.set(k, []);
    byCA.get(k).push(x);
  }
  const multi = [...byCA.entries()].filter(([, v]) => v.length > 1);
  console.log(`総行数 ${rows.length}`);
  console.log(`グループ(会社+住所) ${byCA.size} / うち複数行 ${multi.length}`);

  let needSync = 0; const samples = [];
  for (const [k, v] of multi) {
    const filled = v.filter(x => {
      const t = x.dashboard_todos || {};
      return Object.keys(t).some(kk => SHARED_RE.test(kk) && t[kk]) ||
        (x.p400_status || '').trim() || (x.paycube_status || '').trim();
    });
    if (filled.length > 0 && filled.length < v.length) {
      needSync++;
      if (samples.length < 10) samples.push([k, v, filled]);
    }
  }
  console.log(`片方だけ入力済み = 同期したいグループ: ${needSync}`);

  console.log('\n--- 同期対象サンプル ---');
  for (const [k, v, filled] of samples) {
    const [c, a] = k.split('\u0001');
    console.log(`\n■ ${c} / ${(a || '').replace(/\s+/g, ' ').slice(0, 34)}  (${v.length}行中 ${filled.length}行に入力あり)`);
    for (const x of v) {
      const t = x.dashboard_todos || {};
      const kv = Object.keys(t).filter(kk => SHARED_RE.test(kk) && t[kk]).map(kk => `${kk}=${JSON.stringify(t[kk])}`);
      console.log(`   ${(x.product_name || '').slice(0, 24).padEnd(24)} p400=${JSON.stringify(x.p400_status)} ${kv.join(' , ') || '(共有項目なし)'}`);
    }
  }
})();
