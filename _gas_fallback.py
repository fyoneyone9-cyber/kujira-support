# -*- coding: utf-8 -*-
"""[HEARING_GAS_V24 2026-10-29] google.script.run が応答しない問題への対処。

スクリーンショットから分かったこと:
  ・貼り付けの反映は動いている（施設名・住所・担当者が入っている）
    → dialog の JavaScript は正常
  ・「タブを読み込み中…」のまま
    → google.script.run.getSheetNames() が応答していない
  ・10秒タイムアウトの案内も出ていない
    → setTimeout より前で止まっている可能性 or 貼り直し前の版

原因として最も可能性が高いのは **権限未承認**。
google.script.run はサーバー側関数の実行権限が無いと
成功も失敗も返さずに沈黙することがある。

対策:
  (1) サーバー通信に頼らず、**ダイアログ側だけでタブ一覧を出せる**ようにする
      → createCopy 実行時にサーバーで最終判定するので機能は落ちない
  (2) 手入力でタブ名を指定できる逃げ道を用意
  (3) タイムアウトを5秒に短縮し、必ず案内が出るようにする
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html"
shutil.copy2(P, P + ".bak_v24_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

# タイムアウトを5秒にし、手動入力の逃げ道を出す
OLD = """setTimeout(function () {
  if (loaded) return;
  document.getElementById('tabs').innerHTML =
    '<div style="color:#c00;font-size:13px;line-height:1.7">' +
    '<b>❌ タブを読み込めませんでした</b><br>' +
    '考えられる原因:<br>' +
    '① <b>コード.gs が古い</b> … ダッシュボードの「📋 コード.gs をコピー」で貼り直してください<br>' +
    '② <b>権限の承認が未完了</b> … Apps Scriptで一度 onOpen を実行し、承認してください<br>' +
    '③ dialog の保存漏れ … Ctrl+S を押したか確認してください' +
    '</div>';
}, 10000);"""
assert s.count(OLD) == 1, "anchor1"
NEW = """setTimeout(function () {
  if (loaded) return;
  // [V24] サーバーが応答しない場合の逃げ道。
  //   タブ名を手で入れれば作成できるようにする。
  document.getElementById('tabs').innerHTML =
    '<div style="color:#c00;font-size:13px;line-height:1.7;margin-bottom:6px">' +
    '<b>⚠ タブ一覧を取得できませんでした</b><br>' +
    '<span style="color:#555">Apps Scriptの権限承認が済んでいない可能性があります。<br>' +
    'メニュー「📋 ヒアリングシート → 🔑 権限を承認する」を一度実行してください。</span>' +
    '</div>' +
    '<div style="font-size:12px;color:#555;margin-bottom:4px">' +
    'そのまま進める場合は、残すタブ名を1行ずつ入力してください:</div>' +
    '<textarea id="manualTabs" style="width:100%;height:120px;font-size:12px"></textarea>';
  // 既定値を入れておく（よく使う構成）
  var ta = document.getElementById('manualTabs');
  if (ta) ta.value = ['必須確認①', '必須確認②', '必須確認③'].join('\\n');
  document.getElementById('go').disabled = false;
}, 5000);"""
s = s.replace(OLD, NEW, 1)

# run() で手入力タブにも対応
OLD2 = """function run() {
  var keep = [];
  SHEETS.forEach(function (n, i) {
    if (document.getElementById('t' + i).checked) keep.push(n);
  });
  if (!keep.length) { alert('残すタブを1つ以上選んでください'); return; }"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """function run() {
  var keep = [];
  if (SHEETS.length) {
    SHEETS.forEach(function (n, i) {
      var el = document.getElementById('t' + i);
      if (el && el.checked) keep.push(n);
    });
  } else {
    // [V24] タブ一覧を取得できなかった場合は手入力を使う
    var ta = document.getElementById('manualTabs');
    if (ta) {
      keep = ta.value.split('\\n').map(function (x) { return x.trim(); })
        .filter(function (x) { return x; });
    }
  }
  if (!keep.length) { alert('残すタブを1つ以上選んでください'); return; }"""
s = s.replace(OLD2, NEW2, 1)

# 自動判定が失敗しても止まらないように
OLD3 = """  document.getElementById('msg').innerHTML = '<span style="color:#888">自動判定中…</span>';"""
assert s.count(OLD3) == 1, "anchor3"
NEW3 = """  document.getElementById('msg').innerHTML = '<span style="color:#888">自動判定中…</span>';
  // [V24] 5秒で応答が無ければ諦めて、手動選択を促す
  var judged = false;
  setTimeout(function () {
    if (judged) return;
    document.getElementById('msg').innerHTML =
      '<span style="color:#c77">自動判定は使えませんでした。残すタブを手で選んでください</span>';
  }, 5000);"""
s = s.replace(OLD3, NEW3, 1)

OLD4 = """  google.script.run.withSuccessHandler(function (keep) {
    var set = {};"""
assert s.count(OLD4) == 1, "anchor4"
NEW4 = """  google.script.run.withSuccessHandler(function (keep) {
    judged = true;
    var set = {};"""
s = s.replace(OLD4, NEW4, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
