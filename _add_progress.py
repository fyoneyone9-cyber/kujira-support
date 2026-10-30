# -*- coding: utf-8 -*-
"""[HEARING_GAS_V12 2026-10-29] 進捗表示と完了後の案内を追加する。

指摘:「時間かかるの? 進捗分からないし、このあとどうすればいいかもわからん」

実際の処理:
  雛形コピー(数秒) → 不要シート削除(1枚ずつ数百ms) → 自動入力(17箇所)
  シートが17枚あるので削除だけで10〜20秒、全体で30秒前後かかる。

対策:
  (1) 経過秒数を1秒ごとに表示し、各工程の目安も出す
  (2) 完了後に「このあと何をすればいいか」を明示
  (3) 自動入力のsetValueをまとめて速くする
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html"
bak = P + ".bak_prog_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """function run(){
  var btn = document.getElementById('go');
  btn.disabled = true; btn.textContent = '作成中…';
  document.getElementById('msg').innerHTML = '';"""
assert s.count(OLD) == 1, "anchor1"
NEW = """var timer = null, sec = 0;

/** 経過秒数と工程の目安を出す */
function tick(){
  sec++;
  var step = sec < 8  ? '雛形をコピー中'
           : sec < 25 ? '不要なシートを削除中'
           :            '案件情報を入力中';
  document.getElementById('msg').innerHTML =
    '<b style="color:#1a73e8">⏳ ' + step + '…（' + sec + '秒）</b><br>' +
    '<span style="color:#888;font-size:12px">' +
    '全部で30〜60秒ほどかかります。この画面は閉じないでください</span>';
}

function run(){
  var btn = document.getElementById('go');
  btn.disabled = true; btn.textContent = '作成中…';
  sec = 0;
  if(timer) clearInterval(timer);
  timer = setInterval(tick, 1000);
  tick();"""
s = s.replace(OLD, NEW, 1)

OLD2 = """function done(r){
  var btn = document.getElementById('go');
  btn.disabled = false; btn.textContent = 'コピーを作成';
  document.getElementById('msg').innerHTML =
    '<b style="color:#0b8043">✅ 作成しました</b><br>' +
    '残したシート: ' + r.kept.length + '枚<br>' +
    '削除したシート: ' + r.removed.length + '枚<br>' +
    '自動入力: ' + (r.filled || 0) + '箇所<br>' +
    '<a href="' + r.url + '" target="_blank">▶ 作成したスプレッドシートを開く</a>';
}"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """function done(r){
  if(timer) clearInterval(timer);
  var btn = document.getElementById('go');
  btn.disabled = false; btn.textContent = 'コピーを作成';
  document.getElementById('msg').innerHTML =
    '<div style="background:#e6f4ea;border:1px solid #0b8043;border-radius:6px;padding:10px">' +
    '<b style="color:#0b8043;font-size:15px">✅ 完成しました（' + sec + '秒）</b><br>' +
    '<span style="font-size:12px;color:#555">' +
    '残したシート ' + r.kept.length + '枚 / 削除 ' + r.removed.length + '枚 / ' +
    '自動入力 ' + (r.filled || 0) + '箇所</span>' +
    '<div style="margin-top:8px;padding-top:8px;border-top:1px solid #b7dfc4">' +
    '<b style="font-size:14px">▼ このあとの手順</b><br>' +
    '<a href="' + r.url + '" target="_blank" ' +
    'style="display:inline-block;margin:6px 0;padding:8px 12px;background:#1a73e8;color:#fff;' +
    'border-radius:4px;text-decoration:none;font-weight:bold">▶ 作成したシートを開く</a><br>' +
    '<span style="font-size:12px;color:#555">' +
    '① 開いて内容を確認（空欄はお客様に記入いただく項目です）<br>' +
    '② 右上「共有」またはダウンロードしてお客様へ送付<br>' +
    '③ ダッシュボードの「✉️ 送付メール」から本文をコピーして送信<br>' +
    '保存先: マイドライブ直下「' + r.name + '」</span>' +
    '</div></div>';
}"""
s = s.replace(OLD2, NEW2, 1)

OLD3 = """function fail(e){
  var btn = document.getElementById('go');"""
assert s.count(OLD3) == 1, "anchor3"
NEW3 = """function fail(e){
  if(timer) clearInterval(timer);
  var btn = document.getElementById('go');"""
s = s.replace(OLD3, NEW3, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
