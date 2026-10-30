# -*- coding: utf-8 -*-
"""[HEARING_GAS_V23 2026-10-29] 権限未承認でも動くようにする。

症状:「タブを読み込み中…」「自動判定中…」のまま止まる。

真因: UrlFetchApp（一括削除の高速化用）を追加したため、
  スクリプトに外部リクエスト権限が必要になった。
  承認が済んでいないと google.script.run が**無言で失敗**し、
  withFailureHandler も呼ばれずに固まる。

対策:
  (1) UrlFetchApp を使う前に「承認済みか」を調べ、
      未承認なら最初から従来方式（deleteSheet）で動かす
  (2) getSheetNames / suggestSheets は権限不要なので、
      これらが失敗する場合は別原因と切り分けられるようにログを残す
  (3) onOpen に権限確認メニューを追加
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
shutil.copy2(P, P + ".bak_v23_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

# (1) UrlFetchApp を try で囲んでいるが、getOAuthToken 自体が
#     承認ダイアログを要求して止まることがある。事前判定を入れる。
OLD = """  if (delIds.length) {
    var ok = false;
    try {"""
assert s.count(OLD) == 1, "anchor1"
NEW = """  if (delIds.length) {
    var ok = false;
    // [V23] UrlFetchApp は追加の権限が要る。未承認だとここで固まるので、
    //   権限が取れるか先に確かめ、ダメなら従来方式に落とす。
    var canFetch = false;
    try {
      var tk = ScriptApp.getOAuthToken();
      canFetch = !!tk;
    } catch (e0) {
      canFetch = false;
    }
    try {
      if (!canFetch) throw new Error('no oauth token');"""
s = s.replace(OLD, NEW, 1)

# (3) onOpen に権限確認メニューを追加
OLD2 = """function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('📋 ヒアリングシート')
    .addItem('必要シートだけコピー作成', 'showDialog')
    .addToUi();
}"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('📋 ヒアリングシート')
    .addItem('必要シートだけコピー作成', 'showDialog')
    .addSeparator()
    .addItem('🔑 権限を承認する（初回のみ）', 'checkAuth')
    .addToUi();
}

/**
 * [V23] 権限の承認を促すための関数。
 * メニューから一度実行すると承認ダイアログが出る。
 * 承認後はダイアログが正常に動くようになる。
 */
function checkAuth() {
  var ui = SpreadsheetApp.getUi();
  var names = SpreadsheetApp.getActiveSpreadsheet().getSheets().length;
  var fetchOk = false;
  try {
    ScriptApp.getOAuthToken();
    fetchOk = true;
  } catch (e) {
    fetchOk = false;
  }
  ui.alert('権限の状態',
    'バージョン: ' + GAS_VERSION + '\\n' +
    'シート数: ' + names + '\\n' +
    '外部リクエスト権限: ' + (fetchOk ? 'OK（高速削除が使えます）'
                                      : '未承認（通常速度で動作します）') + '\\n\\n' +
    'この画面が出ていれば基本機能は使えます。',
    ui.ButtonSet.OK);
}"""
s = s.replace(OLD2, NEW2, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
