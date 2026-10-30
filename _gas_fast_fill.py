# -*- coding: utf-8 -*-
"""[HEARING_GAS_V15b 2026-10-29] 自動入力も速くする。

「案件情報を入力中（165秒）」で止まっていたので、fillInfo も重い。
対象3シート×(getValues 2回 + setValues 1回) = 9往復。
各シートの getLastRow/getLastColumn も往復するので実際はもっと多い。

対策: getDataRange().getValues() 1回で済ませ、
      書き込みも必要なときだけ1回にする。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
bak = P + ".bak_v15b_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

i = s.index("  var filled = 0;\n  for (var sheetName in PLAN) {")
j = s.index("  return filled;\n}")

NEW = """  var filled = 0;
  for (var sheetName in PLAN) {
    var sh = ss.getSheetByName(sheetName);
    if (!sh) continue;

    // [V15b] 往復を減らすため、シート全体を1回で読む。
    var values = sh.getDataRange().getValues();
    if (!values.length) continue;

    // 『ご回答欄』の列を探す（シートごとに違う）
    var ansCol = 0;
    for (var r = 0; r < Math.min(6, values.length); r++) {
      for (var c = 0; c < values[r].length; c++) {
        if (String(values[r][c]).indexOf('ご回答欄') >= 0) { ansCol = c + 1; break; }
      }
      if (ansCol) break;
    }
    if (!ansCol) continue;

    // メモリ上で値を決めてから、最後に1回だけ書き込む
    var col = [];
    for (var k = 0; k < values.length; k++) {
      col.push([values[k][ansCol - 1] !== undefined ? values[k][ansCol - 1] : '']);
    }

    var plan = PLAN[sheetName];
    var usedRow = {};
    var changed = false;
    for (var pi = 0; pi < plan.length; pi++) {
      var key = plan[pi][0], val = plan[pi][1];
      if (!val) continue;
      for (var r2 = 0; r2 < values.length; r2++) {
        if (usedRow[r2]) continue;
        if (values[r2].join(' ').indexOf(key) < 0) continue;
        usedRow[r2] = true;
        if (!col[r2][0]) { col[r2][0] = val; filled++; changed = true; }
        break;
      }
    }
    if (changed) sh.getRange(1, ansCol, col.length, 1).setValues(col);
  }
"""
s = s[:i] + NEW + s[j:]
io.open(P, "w", encoding="utf-8").write(s)
print("rewritten fillInfo loop")
