// dialog 内の <script> が構文エラーになっていないか検証する
const fs = require('fs');
const vm = require('vm');
const html = fs.readFileSync('public/docs/hearing-gas-dialog.html', 'utf8');
const m = html.match(/<script>([\s\S]*?)<\/script>/);
if (!m) { console.log('scriptブロックなし'); process.exit(1); }
const code = m[1];
try {
  new vm.Script(code);
  console.log('JS構文: OK  (', code.length, 'bytes )');
} catch (e) {
  console.log('JS構文: NG ->', e.message);
  const line = (e.stack.match(/evalmachine[^:]*:(\d+)/) || [])[1];
  if (line) {
    const ls = code.split('\n');
    const n = Number(line);
    for (let i = Math.max(0, n - 4); i < Math.min(ls.length, n + 3); i++) {
      console.log(`${i + 1 === n ? '>>' : '  '} ${i + 1}| ${ls[i]}`);
    }
  }
  process.exit(1);
}
// 関数の対応も確認
for (const f of ['probe', 'diag', 'applyJson', 'run', 'done', 'fail', 'tick']) {
  console.log(`  function ${f}: ${new RegExp('function\\s+' + f + '\\s*\\(').test(code)}`);
}
