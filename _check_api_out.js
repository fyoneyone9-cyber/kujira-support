// 画面が実際に受け取るAPIレスポンスで dot社のP400表示を再現する
const CSV_BACKED = ['P400', 'PayCube', 'VEGA3000'];
const statusKey = n => n === 'キーボックス' ? 'keybox_status'
  : CSV_BACKED.includes(n) ? `manual_${n.toLowerCase()}_status` : `${n.toLowerCase()}_status`;

(async () => {
  for (const mode of ['', '?mode=alert']) {
    const r = await fetch('http://localhost:3001/api/delivery/items' + mode);
    const j = await r.json();
    const items = j.items || [];
    console.log(`\n=== /api/delivery/items${mode} -> ${r.status}, items=${items.length} ===`);
    if (j.error) { console.log('  error:', j.error); continue; }
    const dot = items.filter(x => (x.client_name || '').includes('dot'));
    for (const x of dot) {
      const manual = (x.dashboard_todos || {})[statusKey('P400')] || null;
      const disp = manual || x.p400_status || null;
      console.log('  dot:', x.product_name);
      console.log('     p400_status      =', JSON.stringify(x.p400_status));
      console.log('     manual_p400_status=', JSON.stringify(manual));
      console.log('     => 表示:', disp || '未発注');
      console.log('     dashboard_todos キー:', Object.keys(x.dashboard_todos || {}).join(', '));
    }
  }
})();
