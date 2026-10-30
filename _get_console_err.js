// ヘッドレスChromeで /delivery を開き、クライアント例外を捕捉する
const { execSync } = require('child_process');
const http = require('http');

// CDP経由: 新規タブを開いてコンソールエラーを拾う
const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PORT = 9333;

const { spawn } = require('child_process');
const proc = spawn(CHROME, [
  '--headless=new', '--disable-gpu', `--remote-debugging-port=${PORT}`,
  '--user-data-dir=C:\\AI\\_cdp_tmp_profile', 'about:blank',
], { detached: true, stdio: 'ignore' });

const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  await sleep(3500);
  const list = await new Promise((res, rej) => {
    http.get(`http://127.0.0.1:${PORT}/json/list`, r => {
      let b = ''; r.on('data', d => b += d); r.on('end', () => res(JSON.parse(b)));
    }).on('error', rej);
  });
  const target = list.find(t => t.type === 'page');
  const WS = require('ws');
  const ws = new WS(target.webSocketDebuggerUrl);
  const errs = [];
  await new Promise(resolve => {
    ws.on('open', () => {
      ws.send(JSON.stringify({ id: 1, method: 'Runtime.enable' }));
      ws.send(JSON.stringify({ id: 2, method: 'Log.enable' }));
      ws.send(JSON.stringify({ id: 3, method: 'Page.enable' }));
      ws.send(JSON.stringify({ id: 4, method: 'Page.navigate',
        params: { url: 'http://localhost:3001/delivery' } }));
      setTimeout(resolve, 15000);
    });
    ws.on('message', d => {
      const m = JSON.parse(d.toString());
      if (m.method === 'Runtime.exceptionThrown') {
        const e = m.params.exceptionDetails;
        errs.push('EXCEPTION: ' + (e.exception && e.exception.description || e.text));
      }
      if (m.method === 'Runtime.consoleAPICalled' && m.params.type === 'error') {
        errs.push('CONSOLE: ' + m.params.args.map(a => a.value || a.description || '').join(' '));
      }
      if (m.method === 'Log.entryAdded' && m.params.entry.level === 'error') {
        errs.push('LOG: ' + m.params.entry.text);
      }
    });
  });
  console.log('--- errors (%d) ---', errs.length);
  errs.slice(0, 15).forEach(e => console.log(e.slice(0, 500)));
  try { process.kill(-proc.pid); } catch (e) {}
  process.exit(0);
})();
