// [MANUAL_EQUIP_STATUS_V2] 再取込で手動値が消えないことの検証。
//   import-csv が更新する列の集合に dashboard_todos が含まれていないことを静的に確認し、
//   実データ上で manual_* が保持されていることを確認する。
const fs = require('fs');
const path = require('path');
const env = {};
for (const line of fs.readFileSync(path.join(__dirname, '.env.local'), 'utf8').split(/\r?\n/)) {
  const m = line.match(/^([A-Z0-9_]+)=(.*)$/);
  if (m) env[m[1]] = m[2].trim();
}
const URL = env.NEXT_PUBLIC_SUPABASE_URL;
const KEY = env.SUPABASE_SERVICE_ROLE_KEY;
const H = { apikey: KEY, Authorization: `Bearer ${KEY}`, 'Content-Type': 'application/json' };

// 1) 静的検査: import-csv が dashboard_todos を書いていないこと
const src = fs.readFileSync(path.join(__dirname, 'src/app/api/delivery/import-csv/route.ts'), 'utf8');
const writesTodos = /dashboard_todos\s*:/.test(src);
console.log(`[1] import-csv writes dashboard_todos ? ${writesTodos ? 'YES (BUG!)' : 'NO  -> OK'}`);

// 2) 静的検査: UI が CSV由来列へ手動値を書いていないこと
const page = fs.readFileSync(path.join(__dirname, 'src/app/(app)/delivery/page.tsx'), 'utf8');
const badField = /getField\s*=\s*\(name: string\)\s*=>\s*\{[\s\S]*?return\s+'p400_status'/.test(page);
console.log(`[2] UI getField returns CSV column ? ${badField ? 'YES (BUG!)' : 'NO  -> OK'}`);

(async () => {
  // 3) 実データ: manual_* を持つ行
  const r = await fetch(`${URL}/rest/v1/delivery_items?select=client_name,p400_status,dashboard_todos&limit=1000`, { headers: H });
  const rows = await r.json();
  const withManual = rows.filter(x => x.dashboard_todos &&
    Object.keys(x.dashboard_todos).some(k => k.startsWith('manual_')));
  console.log(`[3] rows holding manual_* status: ${withManual.length}`);
  for (const x of withManual.slice(0, 10)) {
    const picked = Object.fromEntries(
      Object.entries(x.dashboard_todos).filter(([k]) => k.startsWith('manual_')));
    console.log(`     ${x.client_name}  todos=${JSON.stringify(picked)}  csv.p400_status=${JSON.stringify(x.p400_status)}`);
  }
  const ok = !writesTodos && !badField;
  console.log(`\nRESULT: ${ok ? 'PASS - 再取込してもdashboard_todosは触られない' : 'FAIL'}`);
})();
