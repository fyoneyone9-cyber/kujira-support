// なぜキーボックスが残るのか調べる
const fs = require('fs');

// koutei-gas.js の createKouteiCopy ロジックを確認
const g = fs.readFileSync('public/docs/koutei-gas.js', 'utf8');
const i = g.indexOf('function createKouteiCopy');
console.log('=== createKouteiCopy の削除判定 ===');
console.log(g.slice(i, i + 1200));
