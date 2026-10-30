// 配信中のJSバンドルに新ロジックが入っているか確認する
(async () => {
  const base = 'http://localhost:3001';
  const r = await fetch(base + '/delivery', { redirect: 'follow' });
  const html = await r.text();
  console.log('GET /delivery ->', r.status, 'len=', html.length);

  const srcs = [...html.matchAll(/src="(\/_next\/static\/[^"]+\.js)"/g)].map(m => m[1]);
  console.log('script tags:', srcs.length);

  let hitManual = 0, hitOldField = 0, total = 0;
  const seen = new Set();
  for (const s of srcs) {
    if (seen.has(s)) continue; seen.add(s);
    const j = await fetch(base + s);
    const t = await j.text();
    total += t.length;
    if (t.includes('manual_p400_status')) { hitManual++; console.log('  [NEW] manual_p400_status found in', s); }
    if (/return"p400_status"/.test(t) || /getField[\s\S]{0,200}p400_status"/.test(t)) {
      hitOldField++; console.log('  [OLD] getField->p400_status found in', s);
    }
  }
  console.log(`\nbundles scanned bytes=${total}`);
  console.log(`manual_p400_status 検出: ${hitManual}  (>=1 なら新コードが配信されている)`);
  console.log(`旧 getField 検出:        ${hitOldField} (0 であるべき)`);
})();
