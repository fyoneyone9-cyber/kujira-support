// プリンタ判定を実データで検証する
const fs = require('fs');
const env = fs.readFileSync('.env.local', 'utf8');
const url = (env.match(/NEXT_PUBLIC_SUPABASE_URL=(.+)/) || [])[1].trim();
const key = (env.match(/SUPABASE_SERVICE_ROLE_KEY=(.+)/) || [])[1].trim();

const PRINTER_PAT = /プリンタ|printer/i;

function judge(equipItems) {
  const hasPrinter = equipItems.some(e => PRINTER_PAT.test((e.name || '') + (e.value || '')));
  const hasSurfaceOrKiosk = equipItems.some(e =>
    /surface|KIOSK|キオスク|卓上/i.test((e.name || '') + ' ' + (e.value || '')));
  const isTabletTerminal = equipItems.some(e => {
    const t = (e.name || '') + ' ' + (e.value || '');
    if (/ルームタブレット|room.?tablet/i.test(t)) return false;
    return /タブレット|tablet/i.test(t);
  });
  return { on: hasPrinter || hasSurfaceOrKiosk || !isTabletTerminal, hasPrinter, hasSurfaceOrKiosk, isTabletTerminal };
}

(async () => {
  const r = await fetch(`${url}/rest/v1/delivery_items?select=client_name,equipment&limit=400`, {
    headers: { apikey: key, Authorization: `Bearer ${key}` },
  });
  const rows = await r.json();

  let on = 0, off = 0;
  const offSample = [], tabletSample = [], sfSample = [];
  for (const it of rows) {
    const eq = Array.isArray(it.equipment) ? it.equipment : [];
    const j = judge(eq);
    if (j.on) on++; else { off++; if (offSample.length < 5) offSample.push([it.client_name, eq]); }
    if (j.isTabletTerminal && j.hasSurfaceOrKiosk && sfSample.length < 3) sfSample.push([it.client_name, eq]);
    if (j.isTabletTerminal && !j.hasSurfaceOrKiosk && tabletSample.length < 4) tabletSample.push([it.client_name, eq]);
  }
  console.log(`プリンタ ON: ${on}件 / OFF: ${off}件  (全${rows.length})`);

  console.log('\n--- OFF になる例（タブレット端末）---');
  offSample.forEach(([n, eq]) => console.log(`  ${n}: ${eq.map(e => e.name + '=' + e.value).join(', ').slice(0, 90)}`));

  console.log('\n--- タブレット語ありだがSurface/KIOSKでONになる例 ---');
  sfSample.forEach(([n, eq]) => console.log(`  ${n}: ${eq.map(e => e.name + '=' + e.value).join(', ').slice(0, 90)}`));
  if (!sfSample.length) console.log('  （該当なし）');
})();
