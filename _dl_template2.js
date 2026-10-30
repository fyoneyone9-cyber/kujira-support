// ログイン済みの実プロファイルで雛形をxlsx取得する
const http = require('http');
const fs = require('fs');
const { spawn } = require('child_process');
const WS = require('ws');

const CHROME = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe';
const PORT = 9341;
const ID = '16uW0WLwx-H-KWpCl2zHDstRuQsfcnFyLyLxbRV-_s5E';
const URL = `https://docs.google.com/spreadsheets/d/${ID}/export?format=xlsx`;
const OUT = 'C:\\GensparkClaw\\kujira-support\\_template.xlsx';
const DLDIR = 'C:\\GensparkClaw\\kujira-support\\_dltmp';
const USERDATA = process.env.LOCALAPPDATA + '\\Google\\Chrome\\User Data';
const PROFILE = process.argv[2] || 'Default';

const proc = spawn(CHROME, [
  `--remote-debugging-port=${PORT}`,
  `--user-data-dir=${USERDATA}`,
  `--profile-directory=${PROFILE}`,
  '--no-first-run', '--no-default-browser-check',
  'about:blank',
], { detached: true, stdio: 'ignore' });

const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  fs.mkdirSync(DLDIR, { recursive: true });
  for (const f of fs.readdirSync(DLDIR)) { try { fs.unlinkSync(`${DLDIR}\\${f}`); } catch {} }
  await sleep(5000);
  let list;
  try {
    list = await new Promise((res, rej) =>
      http.get(`http://127.0.0.1:${PORT}/json/list`, r => {
        let b = ''; r.on('data', d => b += d); r.on('end', () => res(JSON.parse(b)));
      }).on('error', rej));
  } catch (e) {
    console.log('CDP接続失敗:', e.message);
    process.exit(1);
  }
  const t = list.find(x => x.type === 'page');
  if (!t) { console.log('page target なし'); process.exit(1); }
  const ws = new WS(t.webSocketDebuggerUrl);
  await new Promise(resolve => {
    ws.on('open', () => {
      ws.send(JSON.stringify({ id: 1, method: 'Page.enable' }));
      ws.send(JSON.stringify({ id: 2, method: 'Page.setDownloadBehavior',
        params: { behavior: 'allow', downloadPath: DLDIR } }));
      ws.send(JSON.stringify({ id: 3, method: 'Page.navigate', params: { url: URL } }));
      setTimeout(resolve, 22000);
    });
  });
  const files = fs.readdirSync(DLDIR).filter(f => f.endsWith('.xlsx'));
  if (files.length) {
    fs.copyFileSync(`${DLDIR}\\${files[0]}`, OUT);
    console.log('OK:', files[0], fs.statSync(OUT).size, 'bytes');
  } else {
    console.log('NG profile=' + PROFILE, 'files:', fs.readdirSync(DLDIR));
  }
  process.exit(0);
})();
