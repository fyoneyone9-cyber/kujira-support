// ビジョン社で equips に何が積まれるかシミュレートし、
// 工程管理表のどの区分が自動チェックされるか検証する
const fs = require('fs');
const env = fs.readFileSync('.env.local', 'utf8');
const url = (env.match(/NEXT_PUBLIC_SUPABASE_URL=(.+)/) || [])[1].trim();
const key = (env.match(/SUPABASE_SERVICE_ROLE_KEY=(.+)/) || [])[1].trim();

// koutei-gas.js の対応表を読む
const g = fs.readFileSync('public/docs/koutei-gas.js', 'utf8');
const blk = g.slice(g.indexOf('var CAT_KEYS'), g.indexOf('var CAT_KEYWORDS'));
const CAT = {};
for (const m of blk.matchAll(/'([^']+)':\s*'(\w+)'/g)) {
  const name = m[1].replace(/\\u([0-9a-f]{4})/gi, (_, h) => String.fromCharCode(parseInt(h, 16)));
  CAT[name] = m[2];
}

(async () => {
  const r = await fetch(
    `${url}/rest/v1/delivery_items?select=client_name,equipment,dashboard_todos&client_name=ilike.*ビジョン*`,
    { headers: { apikey: key, Authorization: `Bearer ${key}` } });
  const rows = (await r.json()).filter(x => x.dashboard_todos?.app_equips);
  if (!rows.length) { console.log('申込書取込済みの案件なし'); return; }
  const it = rows[0];
  const APP = JSON.parse(it.dashboard_todos.app_equips);
  const eqs = it.equipment || [];
  const EQ = re => eqs.some(e => re.test((e.name || '') + ' ' + (e.value || '')));
  const A = k => !!APP[k];
  const hasAPP = true;

  const equips = [];
  const add = (k, v) => { if (v) equips.push(k); };
  add('pms', A('pms'));
  add('smartlock', A('smartlock'));
  add('cardkey', A('cardkey'));
  add('cylinder', EQ(/シリンダー/));
  add('cash', A('paycube'));
  add('p400', A('p400'));
  add('kiosk', A('kiosk'));
  add('kiosk_desk', EQ(/卓上/));
  add('surface', A('surface'));
  add('paycube', A('paycube'));
  add('passport', A('passport'));
  add('keybox', EQ(/キーボックス/));
  add('tablet', EQ(/タブレット/) && !EQ(/ルームタブレット/) && !EQ(/surface/i));
  equips.push('roomtablet' in APP && APP.roomtablet ? 'roomtablet' : null);
  equips.push('sumaho', 'paypay', 'koji');

  const set = new Set(equips.filter(Boolean));
  console.log('申込書の機材:', JSON.stringify(APP));
  console.log('\nequips:', [...set].join(', '));

  console.log('\n=== 工程管理表の区分 判定結果 ===');
  for (const [name, k] of Object.entries(CAT)) {
    const on = k === 'always' || set.has(k);
    console.log(`  ${on ? '✅' : '  '} ${name.padEnd(22)} key=${k}`);
  }
})();
