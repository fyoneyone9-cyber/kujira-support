# -*- coding: utf-8 -*-
"""[HEARING_GAS_V17] 実タブ名方式へ置換（位置はマーカーで特定）。"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
shutil.copy2(P, P + ".bak_v17b_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

i = s.index("var EQUIP_SHEETS")
j = s.index("function showDialog()")
# EQUIP_SHEETS の直前のコメント行も含めて置換したいので、行頭まで戻す
i = s.rfind("\n", 0, i) + 1

NEW = '''/**
 * [V17 2026-10-29] 機材フラグ -> そのシートを示すキーワード
 * シート名の完全一致で判定するとズレて削除漏れが出たので、部分一致にする。
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
 * 実在するタブ名だけを返すので、存在しないシート名を指定する事故が起きない。
 */
function suggestSheets(equips) {
  var names = getSheetNames();
  var keep = [];
  names.forEach(function (n) {
    for (var a = 0; a < ALWAYS_KEYWORDS.length; a++) {
      if (n.indexOf(ALWAYS_KEYWORDS[a]) >= 0) { keep.push(n); return; }
    }
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

# createCopy: 残すタブは配列で受け取る
k = s.index("function createCopy(p) {")
m = s.index("  // 雛形を丸ごとコピー")
s = s[:k] + """function createCopy(p) {
  var src = SpreadsheetApp.getActiveSpreadsheet();

  // [V17] 残すタブ名はダイアログから実タブ名の配列で渡される（ズレない）
  var keep = {};
  (p.sheets || []).forEach(function (n) { keep[n] = true; });

""" + s[m:]

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
