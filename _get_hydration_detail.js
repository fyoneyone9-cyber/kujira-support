// #418 の実際の不一致テキストを取得する（開発ビルドではなくSSR HTMLと比較）
const http = require('http');

(async () => {
  // SSRが返すHTMLを取得
  const html = await new Promise((res, rej) => {
    http.get('http://localhost:3001/delivery', r => {
      let b = ''; r.on('data', d => b += d); r.on('end', () => res(b));
    }).on('error', rej);
  });

  // 時刻っぽい文字列を抽出（SSR側が何を描画しているか）
  const pats = [
    [/\d{2}\/\d{2}\s+\d{2}:\d{2}/g, '日時 MM/DD HH:MM'],
    [/\d+時間未取込/g, 'N時間未取込'],
    [/残\d+日/g, '残N日'],
    [/\d+日超過/g, 'N日超過'],
    [/\d{4}\/\d{1,2}\/\d{1,2}/g, '日付'],
  ];
  console.log('--- SSR HTML に含まれる時刻依存文字列 ---');
  for (const [re, name] of pats) {
    const m = html.match(re);
    if (m) console.log(`  ${name}: ${[...new Set(m)].slice(0, 6).join(', ')} (計${m.length})`);
  }
  console.log('\nHTML長:', html.length);
  // "..." プレースホルダが出ているか（mounted ガードが効いているか）
  console.log('最終取込プレースホルダ "..." :', html.includes('最終取込') ? (html.match(/最終取込[\s\S]{0,200}/) || [''])[0].replace(/<[^>]+>/g, '').slice(0, 80) : 'なし');
})();
