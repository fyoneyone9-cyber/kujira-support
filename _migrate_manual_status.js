// [MANUAL_EQUIP_STATUS_V2 2026-10-29] 既存の手動値を dashboard_todos へ移行する。
//   これまで手動入力は p400_status / paycube_status / vega3000_status (CSV由来列) に
//   書かれていた。今後UIは dashboard_todos.manual_* を読むため、現在値を移しておかないと
//   「今入っている発注済み」が画面上で未発注に見えてしまう。
//   CSV由来列はそのまま残す(フォールバック表示に使う)。非破壊。
//   DRY=1 で変更内容の確認のみ。
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
const DRY = process.env.DRY === '1';

// UIのボタンが出しうる値(EQUIP_STATUSES + PayCube専用)。これ以外はCSV由来とみなす。
const BTN_VOCAB = ['未発注', '発注済み', '入荷履歴', '発送済み', '納品完了', '設定完了', '社長承認待ち']

const MAP = [
  ['P400', 'p400_status', 'manual_p400_status'],
  ['PayCube', 'paycube_status', 'manual_paycube_status'],
  ['VEGA3000', 'vega3000_status', 'manual_vega3000_status'],
];

(async () => {
  const r = await fetch(
    `${URL}/rest/v1/delivery_items?select=id,client_name,p400_status,paycube_status,vega3000_status,dashboard_todos`,
    { headers: H });
  if (!r.ok) { console.error('fetch failed', r.status, await r.text()); process.exit(1); }
  const rows = await r.json();
  console.log('rows:', rows.length);

  let planned = 0;
  for (const row of rows) {
    const todos = row.dashboard_todos || {};
    const add = {};
    for (const [name, csvCol, todoKey] of MAP) {
      const v = (row[csvCol] || '').trim();
      // 【重要】ボタン語彙に完全一致する値だけを移行する。
      //   p400_status には CSV由来の自由記述(日付/送り状番号/「済 2024/04予定」等)も
      //   入っており、それまで todos に移すと今後CSVで更新されなくなる副作用が出る。
      //   手動ボタンで入りうる値だけを「手動値」とみなす。
      if (v && BTN_VOCAB.includes(v) && !todos[todoKey]) add[todoKey] = v;
    }
    if (Object.keys(add).length === 0) continue;
    planned++;
    console.log(`${DRY ? '[DRY] ' : ''}${row.client_name} <- ${JSON.stringify(add)}`);
    if (!DRY) {
      const u = await fetch(`${URL}/rest/v1/delivery_items?id=eq.${row.id}`, {
        method: 'PATCH', headers: H,
        body: JSON.stringify({ dashboard_todos: { ...todos, ...add } }),
      });
      if (!u.ok) console.error('  update failed', u.status, await u.text());
    }
  }
  console.log(`${DRY ? 'would update' : 'updated'}: ${planned} rows`);
})();
