// 「設定をコピー」が出す equips に KIOSK 等が入っているか確認する
const fs = require('fs');
const env = fs.readFileSync('.env.local', 'utf8');
const url = (env.match(/NEXT_PUBLIC_SUPABASE_URL=(.+)/) || [])[1].trim();
const key = (env.match(/SUPABASE_SERVICE_ROLE_KEY=(.+)/) || [])[1].trim();

(async () => {
  const r = await fetch(
    `${url}/rest/v1/delivery_items?select=id,client_name,equipment,dashboard_todos&client_name=ilike.*ビジョン*`,
    { headers: { apikey: key, Authorization: `Bearer ${key}` } });
  const rows = await r.json();
  for (const it of rows) {
    const td = it.dashboard_todos || {};
    if (!td.app_equips) continue;
    console.log(`=== ${it.client_name} ===`);
    console.log('申込書の機材(app_equips):');
    console.log('  ', td.app_equips);
    console.log('CSVのequipment:');
    (it.equipment || []).forEach(e => console.log(`   ${e.name} = ${e.value}`));
    console.log();
  }

  // page.tsx が equips に積むキー一覧を抽出
  const src = fs.readFileSync('src/app/(app)/delivery/page.tsx', 'utf8');
  const i = src.indexOf("const equips: string[] = []");
  if (i < 0) { console.log('equips 生成部が見つからない'); return; }
  console.log('=== 「設定をコピー」が積むキー ===');
  console.log(src.slice(i, i + 1400));
})();
