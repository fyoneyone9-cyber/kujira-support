// SSRのHTMLとハイドレーション後のDOMを比較し、不一致テキストを特定する
const http = require('http');
const { spawn } = require('child_process');
const WS = require('ws');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PORT = 9337;
const proc = spawn(CHROME, ['--headless=new', '--disable-gpu',
  `--remote-debugging-port=${PORT}`, '--user-data-dir=C:\\AI\\_cdp_diff', 'about:blank'],
  { detached: true, stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));

function texts(html) {
  // タグを除いたテキストノードを配列化
  return html
    .replace(/<script[\s\S]*?<\/script>/g, ' ')
    .replace(/<style[\s\S]*?<\/style>/g, ' ')
    .replace(/<[^>]+>/g, '\n')
    .split('\n').map(s => s.trim()).filter(s => s.length > 0 && s.length < 120);
}

(async () => {
  // 1) SSR HTML
  const ssr = await new Promise((res, rej) => {
    http.get('http://localhost:3001/delivery', r => {
      let b = ''; r.on('data', d => b += d); r.on('end', () => res(b));
    }).on('error', rej);
  });

  // 2) ハイドレーション後のDOM
  await sleep(3500);
  const list = await new Promise((res, rej) =>
    http.get(`http://127.0.0.1:${PORT}/json/list`, r => {
      let b = ''; r.on('data', d => b += d); r.on('end', () => res(JSON.parse(b)));
    }).on('error', rej));
  const t = list.find(x => x.type === 'page');
  const ws = new WS(t.webSocketDebuggerUrl);
  const dom = await new Promise(resolve => {
    ws.on('open', () => {
      ws.send(JSON.stringify({ id: 1, method: 'Page.enable' }));
      ws.send(JSON.stringify({ id: 2, method: 'Page.navigate',
        params: { url: 'http://localhost:3001/delivery' } }));
      setTimeout(() => {
        ws.send(JSON.stringify({ id: 3, method: 'Runtime.evaluate',
          params: { expression: 'document.documentElement.outerHTML', returnByValue: true } }));
      }, 14000);
    });
    ws.on('message', d => {
      const m = JSON.parse(d.toString());
      if (m.id === 3) resolve(m.result.result.value || '');
    });
  });

  const a = texts(ssr), b = texts(dom);
  const sa = new Set(a), sb = new Set(b);
  const onlySSR = a.filter(x => !sb.has(x));
  const onlyCSR = b.filter(x => !sa.has(x));

  console.log('--- SSRのみに存在 (消えたテキスト) ---');
  [...new Set(onlySSR)].slice(0, 25).forEach(x => console.log('  -', x));
  console.log('\n--- CSRのみに存在 (後から出たテキスト) ---');
  [...new Set(onlyCSR)].slice(0, 25).forEach(x => console.log('  +', x));

  try { process.kill(-proc.pid); } catch (e) {}
  process.exit(0);
})();
