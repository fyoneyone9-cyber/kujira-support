// 申込書の抽出結果を検証する
const fs = require('fs');
const P = 'C:\\Users\\fyone\\Downloads\\【ADVANCED IOT スマートチェックイン】申込書_株式会社ビジョン御中_20261005.xlsx';

(async () => {
  const buf = fs.readFileSync(P);
  const fd = new FormData();
  fd.append('file', new Blob([buf]), 'app.xlsx');
  const res = await fetch('http://localhost:3001/api/delivery/parse-application', {
    method: 'POST', body: fd,
  });
  console.log('status:', res.status);
  const d = await res.json();
  if (d.error) { console.log('ERR:', d.error); return; }

  console.log('\n=== 抽出した案件情報 ===');
  for (const k of ['client', 'clientAddress', 'contact', 'billingAddress',
    'facility', 'siteAddress', 'tel', 'email', 'due', 'rooms']) {
    console.log(`  ${k.padEnd(16)} ${d[k] || '(空)'}`);
  }
  console.log('  tels            ', (d.tels || []).join(' / '));
  console.log('  emails          ', (d.emails || []).join(' / '));

  console.log('\n=== 機材構成 ===');
  Object.entries(d.equips || {}).forEach(([k, v]) => console.log(`  ${k.padEnd(12)} x${v}`));

  console.log('\n=== 費用明細（先頭12件）===');
  (d.items || []).slice(0, 12).forEach(x =>
    console.log(`  ${String(x.name).slice(0, 42).padEnd(44)} ${String(x.price).padStart(8)} x${x.qty}`));
})();
