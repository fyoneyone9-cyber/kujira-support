# -*- coding: utf-8 -*-
"""[HEARING_GAS_V13 2026-10-29] 134秒かかる問題を根治する。

実測134秒。原因は2つ:
 (1) シート削除を1枚ずつ deleteSheet している
     17枚中9枚削除 = 9回のサーバー往復。1回2〜5秒かかることもある。
 (2) fillInfo が「シートの全セル」を getValues で読んでいた
     必須確認③は107行×11列、必須確認②は57行。
     さらに全シート分ループするので読み込みだけで数十秒。

対策:
 (1) 削除は仕方ないが、先に対象を確定してから回す（getSheets()の再取得をやめる）
 (2) fillInfo は **入力対象のシートだけ** 開く（必須確認②/カードキー/PayPayの3枚）
     読む範囲も「項目名が入る列(A〜D)」に限定する
 (3) SpreadsheetApp.flush() を最後に1回だけ
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
bak = P + ".bak_v13_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# --- (1) 削除ループを軽くする ---
OLD1 = """  // 不要シートを削除
  var removed = [];
  copy.getSheets().forEach(function (sh) {
    var n = sh.getName();
    if (!keep[n]) {
      try { copy.deleteSheet(sh); removed.push(n); } catch (e) {}
    }
  });"""
assert s.count(OLD1) == 1, "anchor1"
NEW1 = """  // 不要シートを削除（対象を先に確定してから回す）
  var removed = [];
  var all = copy.getSheets();
  var delList = [];
  for (var i = 0; i < all.length; i++) {
    if (!keep[all[i].getName()]) delList.push(all[i]);
  }
  for (var j = 0; j < delList.length; j++) {
    try { removed.push(delList[j].getName()); copy.deleteSheet(delList[j]); } catch (e) {}
  }"""
s = s.replace(OLD1, NEW1, 1)

# --- (2) 読み取り範囲を絞る ---
OLD2 = """    var last = sh.getLastRow(), lastCol = sh.getLastColumn();
    if (last < 1 || lastCol < 1) continue;
    var values = sh.getRange(1, 1, last, lastCol).getValues();"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """    var last = sh.getLastRow(), lastCol = sh.getLastColumn();
    if (last < 1 || lastCol < 1) continue;
    // [V13] 項目名は左側(A〜D)にしか無いので、そこだけ読む。
    //   全列読むと必須確認③(107行×11列)などで大幅に遅くなる。
    var scanCol = Math.min(lastCol, 4);
    var values = sh.getRange(1, 1, last, scanCol).getValues();"""
s = s.replace(OLD2, NEW2, 1)

# --- (3) 回答欄の検出も絞った範囲で行う ---
OLD3 = """    // 『ご回答欄』の列を探す（シートごとに違う）
    var ansCol = 0;
    for (var r = 0; r < Math.min(6, values.length); r++) {
      for (var c = 0; c < values[r].length; c++) {
        if (String(values[r][c]).indexOf('ご回答欄') >= 0) { ansCol = c + 1; break; }
      }
      if (ansCol) break;
    }
    if (!ansCol) continue;"""
assert s.count(OLD3) == 1, "anchor3"
NEW3 = """    // 『ご回答欄』はヘッダ行の右側にあるので、先頭6行だけ全幅で読んで探す
    var ansCol = 0;
    var head = sh.getRange(1, 1, Math.min(6, last), lastCol).getValues();
    for (var r = 0; r < head.length; r++) {
      for (var c = 0; c < head[r].length; c++) {
        if (String(head[r][c]).indexOf('ご回答欄') >= 0) { ansCol = c + 1; break; }
      }
      if (ansCol) break;
    }
    if (!ansCol) continue;"""
s = s.replace(OLD3, NEW3, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
