// キャッシュを無効化して再検証する
const http = require('http');
const { spawn } = require('child_process');
const WS = require('ws');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PORT = 9335;
const proc = spawn(CHROME, ['--headless=new', '--disable-gpu',
  `--remote-debugging-port=${PORT}`,
  '--user-data-dir=C:\\AI\\_cdp_tmp_profile3', 'about:blank'],
  { detached: true, stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  await sleep(3500);
  const list = await new Promise((res, rej) =>
    http.get(`http://127.0.0.1:${PORT}/json/list`, r => {
      let b = ''; r.on('data', d => b += d); r.on('end', () => res(JSON.parse(b)));
    }).on('error', rej));
  const t = list.find(x => x.type === 'page');
  const ws = new WS(t.webSocketDebuggerUrl);
  const out = [];
  let okJs = 0;
  await new Promise(resolve => {
    ws.on('open', () => {
      ws.send(JSON.stringify({ id: 1, method: 'Runtime.enable' }));
      ws.send(JSON.stringify({ id: 2, method: 'Network.enable' }));
      ws.send(JSON.stringify({ id: 3, method: 'Network.setCacheDisabled',
        params: { cacheDisabled: true } }));
      setTimeout(() => ws.send(JSON.stringify({ id: 9, method: 'Page.navigate',
        params: { url: 'http://localhost:3001/delivery' } })), 500);
      setTimeout(resolve, 16000);
    });
    ws.on('message', d => {
      const m = JSON.parse(d.toString());
      if (m.method === 'Network.responseReceived') {
        const u = m.params.response.url, st = m.params.response.status;
        if (st >= 400) out.push(`HTTP ${st}  ${u}`);
        else if (u.includes('/delivery/page-')) { okJs++; out.push(`OK ${st}  ${u.split('/').pop()}`); }
      }
      if (m.method === 'Runtime.exceptionThrown') {
        const e = m.params.exceptionDetails;
        out.push('EXC: ' + ((e.exception && e.exception.description) || e.text || '').slice(0, 400));
      }
      if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') {
        out.push('ERRLOG: ' + m.params.args.map(a => a.description || a.value || '').join(' ').slice(0, 400));
      }
    });
  });
  out.slice(0, 20).forEach(x => console.log(x));
  console.log('--- errors/notes:', out.length);
  try { process.kill(-proc.pid); } catch (e) {}
  process.exit(0);
})();
