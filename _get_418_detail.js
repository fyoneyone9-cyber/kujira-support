// 開発サーバ(3099)を立て、#418 の詳細メッセージ（どのテキストが不一致か）を取得する
const http = require('http');
const { spawn } = require('child_process');
const WS = require('ws');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PORT = 9336;
const proc = spawn(CHROME, ['--headless=new', '--disable-gpu',
  `--remote-debugging-port=${PORT}`,
  '--user-data-dir=C:\\AI\\_cdp_tmp_p418', 'about:blank'],
  { detached: true, stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
const TARGET = process.argv[2] || 'http://localhost:3099/delivery';

(async () => {
  await sleep(3500);
  const list = await new Promise((res, rej) =>
    http.get(`http://127.0.0.1:${PORT}/json/list`, r => {
      let b = ''; r.on('data', d => b += d); r.on('end', () => res(JSON.parse(b)));
    }).on('error', rej));
  const t = list.find(x => x.type === 'page');
  const ws = new WS(t.webSocketDebuggerUrl);
  const out = [];
  await new Promise(resolve => {
    ws.on('open', () => {
      ws.send(JSON.stringify({ id: 1, method: 'Runtime.enable' }));
      ws.send(JSON.stringify({ id: 2, method: 'Page.enable' }));
      setTimeout(() => ws.send(JSON.stringify({ id: 9, method: 'Page.navigate',
        params: { url: TARGET } })), 400);
      setTimeout(resolve, 30000);
    });
    ws.on('message', d => {
      const m = JSON.parse(d.toString());
      if (m.method === 'Runtime.consoleAPICalled') {
        const txt = m.params.args.map(a => a.value || a.description || '').join(' ');
        if (/hydrat|418|mismatch|did not match|Warning/i.test(txt)) out.push('[' + m.params.type + '] ' + txt.slice(0, 1500));
      }
      if (m.method === 'Runtime.exceptionThrown') {
        const e = m.params.exceptionDetails;
        out.push('EXC: ' + ((e.exception && e.exception.description) || e.text || '').slice(0, 1500));
      }
    });
  });
  out.slice(0, 6).forEach(x => { console.log('\n======'); console.log(x); });
  console.log('\n--- total', out.length);
  try { process.kill(-proc.pid); } catch (e) {}
  process.exit(0);
})();
