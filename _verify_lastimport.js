// 修正後のロジックを再現し、画面に出る「最終取込」を検証する
const fs = require('fs'); const path = require('path');
const env = {};
for (const line of fs.readFileSync(path.join(__dirname, '.env.local'), 'utf8').split(/\r?\n/)) {
  const m = line.match(/^([A-Z0-9_]+)=(.*)$/); if (m) env[m[1]] = m[2].trim();
}

(async () => {
  const r = await fetch('http://localhost:3001/api/delivery/items');
  const j = await r.json();
  const all = j.items || [];
  console.log('items:', all.length);

  // 修正前（誤）
  const oldVal = all.length > 0
    ? all.reduce((a, b) => (a.created_at > b.created_at ? a : b)).created_at : null;
  // 修正後（正）
  const newVal = all.length > 0
    ? (all.map(x => x.last_imported_at).filter(Boolean).sort().slice(-1)[0] || null) : null;

  const fmt = v => v ? new Date(v).toLocaleString('ja-JP') : 'null';
  const hrs = v => v ? ((Date.now() - new Date(v).getTime()) / 3600000).toFixed(1) : '-';

  console.log('\n修正前(created_at)     :', fmt(oldVal), ' /', hrs(oldVal), '時間前');
  console.log('修正後(last_imported_at):', fmt(newVal), ' /', hrs(newVal), '時間前');
  console.log('\n24時間アラート: 修正前=' + (hrs(oldVal) >= 24) + ' / 修正後=' + (hrs(newVal) >= 24));
})();
