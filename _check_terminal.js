// 端末種別（KIOSK/Surface/タブレット）が実データでどう入っているか確認する
const fs = require('fs');
const env = fs.readFileSync('.env.local', 'utf8');
const url = (env.match(/NEXT_PUBLIC_SUPABASE_URL=(.+)/) || [])[1].trim();
const key = (env.match(/SUPABASE_SERVICE_ROLE_KEY=(.+)/) || [])[1].trim();

(async () => {
  const r = await fetch(`${url}/rest/v1/delivery_items?select=client_name,product_name,equipment&limit=400`, {
    headers: { apikey: key, Authorization: `Bearer ${key}` },
  });
  const rows = await r.json();
  console.log('件数:', rows.length);

  const bag = {};
  for (const it of rows) {
    const txt = JSON.stringify(it.equipment || '') + ' ' + (it.product_name || '');
    for (const kw of ['KIOSK', 'キオスク', '卓上', 'Surface', 'surface', 'タブレット', 'プリンタ']) {
      if (txt.includes(kw)) bag[kw] = (bag[kw] || 0) + 1;
    }
  }
  console.log('\n出現回数:');
  Object.entries(bag).sort((a, b) => b[1] - a[1]).forEach(([k, v]) => console.log(`  ${k.padEnd(12)} ${v}`));

  console.log('\n--- equipment のサンプル3件 ---');
  rows.filter(x => x.equipment).slice(0, 3).forEach(x => {
    console.log(` ${x.client_name}: ${JSON.stringify(x.equipment).slice(0, 220)}`);
  });
})();
