// 申込書の取り込み結果がDBに保存されているか確認する
const fs = require('fs');
const env = fs.readFileSync('.env.local', 'utf8');
const url = (env.match(/NEXT_PUBLIC_SUPABASE_URL=(.+)/) || [])[1].trim();
const key = (env.match(/SUPABASE_SERVICE_ROLE_KEY=(.+)/) || [])[1].trim();

(async () => {
  const r = await fetch(
    `${url}/rest/v1/delivery_items?select=id,client_name,dashboard_todos&client_name=ilike.*ビジョン*`,
    { headers: { apikey: key, Authorization: `Bearer ${key}` } });
  const rows = await r.json();
  console.log('ビジョン案件:', rows.length, '件\n');
  for (const it of rows) {
    const td = it.dashboard_todos || {};
    const appKeys = Object.keys(td).filter(k => k.startsWith('app_'));
    console.log(`id=${it.id}  ${it.client_name}`);
    if (appKeys.length) {
      appKeys.forEach(k => console.log(`    ${k.padEnd(18)} ${String(td[k]).slice(0, 50)}`));
    } else {
      console.log('    app_* なし');
    }
    console.log(`    dashboard_todos のキー数: ${Object.keys(td).length}`);
  }
})();
