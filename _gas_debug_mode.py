# -*- coding: utf-8 -*-
"""[HEARING_GAS_V25 2026-10-29] 原因を画面に出して特定する。

承認済みなのに google.script.run が応答しない。
推測で潰すのをやめ、**実際のエラーを画面に表示**する。

よくある原因:
  ・dialog と コード.gs のどちらかが古い（片方だけ貼った）
  ・コード.gs に構文エラーがあり、全関数が読み込まれていない
  ・関数名のタイポ

対策: 画面上部に診断パネルを出し、
  各関数の呼び出し結果（成功/失敗/エラー文）をその場に表示する。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html"
shutil.copy2(P, P + ".bak_v25_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

# 診断パネルを追加
OLD = """<h3>必要シートだけコピー作成 <span id="ver" style="font-size:11px;color:#888;font-weight:normal"></span></h3>"""
assert s.count(OLD) == 1, "anchor1"
NEW = """<h3>必要シートだけコピー作成 <span id="ver" style="font-size:11px;color:#888;font-weight:normal"></span></h3>
<div id="diag" style="font-size:11px;background:#f5f5f5;border:1px solid #ddd;border-radius:4px;padding:6px;margin-bottom:8px;font-family:monospace;white-space:pre-wrap">診断中…</div>"""
s = s.replace(OLD, NEW, 1)

# 診断ロジックを先頭に入れる
OLD2 = """// [V22] コード側のバージョンを表示（新旧の貼り間違いを一目で判別する）"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """// [V25 2026-10-29] 原因特定のための診断。各関数の結果を画面に出す。
var diagLog = [];
function diag(msg) {
  diagLog.push(msg);
  var el = document.getElementById('diag');
  if (el) el.textContent = diagLog.join('\\n');
}
diag('dialog 読込OK (V25)');

// サーバー関数を1つずつ試して、どこで落ちるか突き止める
function probe(name, fn, arg) {
  var done = false;
  setTimeout(function () {
    if (!done) diag('  ' + name + ' : 応答なし（5秒）');
  }, 5000);
  try {
    var runner = google.script.run
      .withSuccessHandler(function (r) {
        done = true;
        diag('  ' + name + ' : OK ' + (Array.isArray(r) ? '(' + r.length + '件)' : String(r).slice(0, 40)));
        if (fn) fn(r);
      })
      .withFailureHandler(function (e) {
        done = true;
        diag('  ' + name + ' : 失敗 -> ' + (e && e.message ? e.message : String(e)));
      });
    if (arg !== undefined) runner[name](arg); else runner[name]();
  } catch (err) {
    done = true;
    diag('  ' + name + ' : 呼び出し例外 -> ' + err);
  }
}

if (typeof google === 'undefined' || !google.script || !google.script.run) {
  diag('❌ google.script.run が使えません（Apps Script外で開いています）');
} else {
  diag('google.script.run OK');
}

// [V22] コード側のバージョンを表示（新旧の貼り間違いを一目で判別する）"""
s = s.replace(OLD2, NEW2, 1)

# getVersion / getSheetNames を probe 経由に
OLD3 = """google.script.run.withSuccessHandler(function (v) {
  document.getElementById('ver').textContent = '[' + v + ']';
}).withFailureHandler(function () {
  document.getElementById('ver').textContent = '[コードが古い可能性あり]';
}).getVersion();"""
assert s.count(OLD3) == 1, "anchor3"
NEW3 = """probe('getVersion', function (v) {
  document.getElementById('ver').textContent = '[' + v + ']';
});"""
s = s.replace(OLD3, NEW3, 1)

OLD4 = """/** 起動時に実タブ名を読み込む */
google.script.run.withSuccessHandler(function (names) {
  loaded = true;"""
assert s.count(OLD4) == 1, "anchor4"
NEW4 = """/** 起動時に実タブ名を読み込む */
probe('getSheetNames', function (names) {
  loaded = true;
  (function (names) {"""
s = s.replace(OLD4, NEW4, 1)

OLD5 = """  document.getElementById('go').disabled = false;
}).withFailureHandler(function (e) {
  document.getElementById('tabs').innerHTML =
    '<span style="color:#c00">タブの読み込みに失敗: ' + e.message + '</span>';
}).getSheetNames();"""
assert s.count(OLD5) == 1, "anchor5"
NEW5 = """  document.getElementById('go').disabled = false;
  })(names);
});"""
s = s.replace(OLD5, NEW5, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
