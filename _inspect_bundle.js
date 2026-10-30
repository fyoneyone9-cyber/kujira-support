// 配信バンドル内の getStatus/getField/statusKey 相当のコードを抜き出して目視確認する
const fs = require('fs');
const p = String.raw`C:\GensparkClaw\kujira-support\.next\static\chunks\app\(app)\delivery\page-963aa4eca2ac4117.js`;
const t = fs.readFileSync(p, 'utf8');
console.log('bundle bytes:', t.length);

for (const kw of ['manual_', 'keybox_status', 'p400_status', 'paycube_status', '_status"']) {
  const n = (t.match(new RegExp(kw.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g')) || []).length;
  console.log(`  "${kw}" x${n}`);
}

// manual_ 周辺を抜き出す
let i = 0, shown = 0;
while ((i = t.indexOf('manual_', i + 1)) > 0 && shown < 6) {
  console.log('\n--- around manual_ @' + i + ' ---');
  console.log(t.slice(Math.max(0, i - 420), i + 320).replace(/\n/g, ' '));
  shown++;
}
