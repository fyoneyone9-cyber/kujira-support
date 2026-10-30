# -*- coding: utf-8 -*-
"""[HEARING_GAS_V17 2026-10-29] 実タブ名を読んで選ばせる方式に変更する。

問題: シート名の完全一致で判定していたため、1文字でも違うと
      「知らないシート」になり残ってしまった。
      例: スマホカード決済 がコードにあるが雛形には無い、など。

新方式:
  (1) getSheetNames() で実際のタブ名を返す
  (2) ダイアログはそれを一覧表示（存在するものしか出ない＝ズレない）
  (3) 自動チェックは「キーワード照合」で行う
      機材フラグ -> そのシートを示すキーワード、で部分一致させる
      → 名前が多少違っても拾える
  (4) ユーザーが最終的にチェックを調整できる
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
bak = P + ".bak_v17_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# EQUIP_SHEETS を「キーワード表」に置き換える
i = s.index("/** 機材 -> 必要シート の対応。ダッシュボードの判定と同じ。 */")
j = s.index("function showDialog()")

NEW = '''/**
 * [V17] 機材フラグ -> そのシートを示すキーワード
 * シート名の完全一致はズレるので、部分一致で判定する。
 */
var EQUIP_KEYWORDS = {
  pms:        ['PMS'],
  smartlock:  ['スマートロック'],
  cardkey:    ['カードキー'],
  cylinder:   ['シリンダー'],
  cash:       ['現金'],
  p400:       ['端末カード'],
  sumaho:     ['スマホカード', 'スマートカード'],
  paypay:     ['PayPay', 'ペイペイ'],
  printer:    ['プリンタ'],
  roomtablet: ['ルームタブレット'],
  precheckin: ['事前チェックイン']
};

/** 常に残すシートのキーワード */
var ALWAYS_KEYWORDS = ['必須確認', '表紙'];

/** 実際のタブ名を返す（ダイアログが一覧表示に使う） */
function getSheetNames() {
  return SpreadsheetApp.getActiveSpreadsheet().getSheets().map(function (sh) {
    return sh.getName();
  });
}

/**
 * 機材フラグから「残すべきタブ名」を推定する。
 * ダイアログ側で自動チェックを入れるために使う。
 * @param {string[]} equips 機材キーの配列
 * @return {string[]} 残すタブ名
 */
function suggestSheets(equips) {
  var names = getSheetNames();
  var keep = [];
  names.forEach(function (n) {
    // 常に残すもの
    for (var a = 0; a < ALWAYS_KEYWORDS.length; a++) {
      if (n.indexOf(ALWAYS_KEYWORDS[a]) >= 0) { keep.push(n); return; }
    }
    // 機材に対応するもの
    for (var e = 0; e < (equips || []).length; e++) {
      var kws = EQUIP_KEYWORDS[equips[e]] || [];
      for (var k = 0; k < kws.length; k++) {
        if (n.indexOf(kws[k]) >= 0) { keep.push(n); return; }
      }
    }
  });
  return keep;
}

'''
s = s[:i] + NEW + s[j:]

# createCopy を「タブ名の配列を受け取る」方式に
k = s.index("function createCopy(p) {")
m = s.index("  // 雛形を丸ごとコピー")
NEW2 = """function createCopy(p) {
  var src = SpreadsheetApp.getActiveSpreadsheet();

  // [V17] 残すタブ名はダイアログから配列で渡される（実タブ名なのでズレない）
  var keep = {};
  (p.sheets || []).forEach(function (n) { keep[n] = true; });

"""
s = s[:k] + NEW2 + s[m:]

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
