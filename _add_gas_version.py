# -*- coding: utf-8 -*-
"""[HEARING_GAS_V22 2026-10-29] バージョン表示とエラー可視化を追加する。

症状:「タブを読み込み中…」「自動判定中…」のまま止まる
原因候補:
  (1) 貼り付けたコードが古く getSheetNames / suggestSheets が無い
  (2) 権限承認が済んでおらず google.script.run が失敗している
  (3) エラーが出ているが withFailureHandler が効いていない

対策:
  ・ダイアログにコード側のバージョンを表示し、新旧を判別できるようにする
  ・失敗時に「何が起きたか」と対処法を画面に出す
  ・10秒応答が無ければタイムアウト扱いにして案内を出す
"""
import io, shutil, datetime

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# ---- GAS: バージョンを返す ----
P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
shutil.copy2(P, P + ".bak_v22_" + ts)
g = io.open(P, encoding="utf-8").read()

OLD = "/** 実際のタブ名を返す（ダイアログが一覧表示に使う） */"
assert g.count(OLD) == 1, "anchor gas"
NEW = """/** このコードのバージョン。ダイアログに表示して新旧を判別する。 */
var GAS_VERSION = 'V22 2026-10-29';

/** 実際のタブ名を返す（ダイアログが一覧表示に使う） */"""
g = g.replace(OLD, NEW, 1)

OLD2 = """function getSheetNames() {
  return SpreadsheetApp.getActiveSpreadsheet().getSheets().map(function (sh) {
    return sh.getName();
  });
}"""
assert g.count(OLD2) == 1, "anchor getSheetNames"
NEW2 = """function getSheetNames() {
  return SpreadsheetApp.getActiveSpreadsheet().getSheets().map(function (sh) {
    return sh.getName();
  });
}

/** バージョン確認用（ダイアログが最初に呼ぶ） */
function getVersion() {
  return GAS_VERSION;
}"""
g = g.replace(OLD2, NEW2, 1)
io.open(P, "w", encoding="utf-8").write(g)
print("GAS: getVersion を追加")

# ---- dialog: 失敗を可視化 ----
D = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html"
shutil.copy2(D, D + ".bak_v22_" + ts)
d = io.open(D, encoding="utf-8").read()

OLD3 = """/** 起動時に実タブ名を読み込む */
google.script.run.withSuccessHandler(function (names) {"""
assert d.count(OLD3) == 1, "anchor dialog1"
NEW3 = """/** [V22] 応答が無いまま止まる事故を防ぐため、10秒でタイムアウト案内を出す */
var loaded = false;
setTimeout(function () {
  if (loaded) return;
  document.getElementById('tabs').innerHTML =
    '<div style="color:#c00;font-size:13px;line-height:1.7">' +
    '<b>❌ タブを読み込めませんでした</b><br>' +
    '考えられる原因:<br>' +
    '① <b>コード.gs が古い</b> … ダッシュボードの「📋 コード.gs をコピー」で貼り直してください<br>' +
    '② <b>権限の承認が未完了</b> … Apps Scriptで一度 onOpen を実行し、承認してください<br>' +
    '③ dialog の保存漏れ … Ctrl+S を押したか確認してください' +
    '</div>';
}, 10000);

/** 起動時に実タブ名を読み込む */
google.script.run.withSuccessHandler(function (names) {
  loaded = true;"""
d = d.replace(OLD3, NEW3, 1)

# バージョン表示
OLD4 = """<h3>必要シートだけコピー作成</h3>"""
assert d.count(OLD4) == 1, "anchor dialog2"
NEW4 = """<h3>必要シートだけコピー作成 <span id="ver" style="font-size:11px;color:#888;font-weight:normal"></span></h3>"""
d = d.replace(OLD4, NEW4, 1)

OLD5 = """var SHEETS = [];      // 実タブ名"""
assert d.count(OLD5) == 1, "anchor dialog3"
NEW5 = """// [V22] コード側のバージョンを表示（新旧の貼り間違いを一目で判別する）
google.script.run.withSuccessHandler(function (v) {
  document.getElementById('ver').textContent = '[' + v + ']';
}).withFailureHandler(function () {
  document.getElementById('ver').textContent = '[コードが古い可能性あり]';
}).getVersion();

var SHEETS = [];      // 実タブ名"""
d = d.replace(OLD5, NEW5, 1)

# suggestSheets 失敗時の案内を具体的に
OLD6 = """    document.getElementById('msg').innerHTML =
      '<span style="color:#c00">自動判定に失敗: ' + e.message + '</span>';"""
assert d.count(OLD6) == 1, "anchor dialog4"
NEW6 = """    document.getElementById('msg').innerHTML =
      '<span style="color:#c00"><b>❌ 自動判定に失敗</b><br>' + e.message + '<br>' +
      'コード.gs が古い可能性があります。貼り直して Ctrl+S してください</span>';"""
d = d.replace(OLD6, NEW6, 1)

io.open(D, "w", encoding="utf-8").write(d)
print("dialog: タイムアウト案内とバージョン表示を追加")
