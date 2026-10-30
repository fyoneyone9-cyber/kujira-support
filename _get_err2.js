// 400を返しているURLと、実際のJSエラーを特定する
const http = require('http');
const { spawn } = require('child_process');
const WS = require('ws');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PORT = 9334;
const proc = spawn(CHROME, ['--headless=new', '--disable-gpu',
  `--remote-debugging-port=${PORT}`,
  '--user-data-dir=C:\\AI\\_cdp_tmp_profile2', 'about:blank'],
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
  const reqs = {};
  await new Promise(resolve => {
    ws.on('open', () => {
      ['Runtime.enable', 'Network.enable', 'Page.enable'].forEach((mth, i) =>
        ws.send(JSON.stringify({ id: i + 1, method: mth })));
      ws.send(JSON.stringify({ id: 9, method: 'Page.navigate',
        params: { url: 'http://localhost:3001/delivery' } }));
      setTimeout(resolve, 16000);
    });
    ws.on('message', d => {
      const m = JSON.parse(d.toString());
      if (m.method === 'Network.requestWillBeSent') reqs[m.params.requestId] = m.params.request.url;
      if (m.method === 'Network.responseReceived' && m.params.response.status >= 400) {
        out.push(`HTTP ${m.params.response.status}  ${m.params.response.url}`);
      }
      if (m.method === 'Runtime.exceptionThrown') {
        const e = m.params.exceptionDetails;
        out.push('EXC: ' + ((e.exception && e.exception.description) || e.text || '').slice(0, 600));
      }
      if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') {
        out.push('ERRLOG: ' + m.params.args.map(a =>
          a.description || a.value || JSON.stringify(a.preview || '')).join(' ').slice(0, 600));
      }
    });
  });
  out.slice(0, 20).forEach(x => console.log(x));
  console.log('--- total', out.length);
  try { process.kill(-proc.pid); } catch (e) {}
  process.exit(0);
})();
