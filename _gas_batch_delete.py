# -*- coding: utf-8 -*-
"""[HEARING_GAS_V15 2026-10-29] 165秒 → 数秒に短縮する。

真因: SpreadsheetApp.deleteSheet() は1枚ごとにサーバー往復が発生する。
      9枚削除で数十秒〜。さらにシートが大きいと1枚10秒以上かかることもある。

対策: Sheets API の batchUpdate を UrlFetchApp で直接叩き、
      **全シートの削除を1リクエストにまとめる**。
      ScriptApp.getOAuthToken() を使うので追加設定は不要。
      失敗したら従来方式にフォールバックする。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
bak = P + ".bak_v15_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """  // 不要シートを削除（対象を先に確定してから回す）
  var removed = [];
  var all = copy.getSheets();
  var delList = [];
  for (var i = 0; i < all.length; i++) {
    if (!keep[all[i].getName()]) delList.push(all[i]);
  }
  for (var j = 0; j < delList.length; j++) {
    try { removed.push(delList[j].getName()); copy.deleteSheet(delList[j]); } catch (e) {}
  }"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)

NEW = """  // 不要シートを削除
  // [V15] deleteSheet() を1枚ずつ呼ぶと往復が多くて非常に遅い（実測165秒）。
  //   Sheets API の batchUpdate で**1リクエストにまとめて**削除する。
  var removed = [];
  var all = copy.getSheets();
  var delIds = [];
  for (var i = 0; i < all.length; i++) {
    if (!keep[all[i].getName()]) {
      delIds.push(all[i].getSheetId());
      removed.push(all[i].getName());
    }
  }

  if (delIds.length) {
    var ok = false;
    try {
      var reqs = delIds.map(function (id) {
        return { deleteSheet: { sheetId: id } };
      });
      var res = UrlFetchApp.fetch(
        'https://sheets.googleapis.com/v4/spreadsheets/' + copy.getId() + ':batchUpdate',
        {
          method: 'post',
          contentType: 'application/json',
          headers: { Authorization: 'Bearer ' + ScriptApp.getOAuthToken() },
          payload: JSON.stringify({ requests: reqs }),
          muteHttpExceptions: true
        });
      ok = (res.getResponseCode() === 200);
      if (!ok) Logger.log('batchUpdate failed: ' + res.getContentText());
    } catch (e) {
      Logger.log('batchUpdate error: ' + e);
    }

    // 一括削除が使えない環境では従来方式にフォールバック
    if (!ok) {
      removed = [];
      var again = copy.getSheets();
      for (var j = 0; j < again.length; j++) {
        if (!keep[again[j].getName()]) {
          try { removed.push(again[j].getName()); copy.deleteSheet(again[j]); } catch (e2) {}
        }
      }
    }
  }"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
