# -*- coding: utf-8 -*-
"""[HEARING_GAS_V12b 2026-10-29] 処理を速くする。

遅い原因:
  ・fillInfo が項目ごとに getRange().getValue() / setValue() を呼んでいた
    → 1回ごとにサーバー往復が発生し、17箇所で34往復
  ・シート削除も1枚ずつ

対策:
  ・回答欄の列をまとめて読み(getValues)、まとめて書く(setValues)
  ・往復回数を シート数×2 に削減
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
bak = P + ".bak_speed_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """    var plan = PLAN[sheetName];
    var usedRow = {};
    for (var pi = 0; pi < plan.length; pi++) {
      var key = plan[pi][0], val = plan[pi][1];
      if (!val) continue;
      for (var r2 = 0; r2 < values.length; r2++) {
        if (usedRow[r2]) continue;
        if (values[r2].join(' ').indexOf(key) < 0) continue;
        var cell = sh.getRange(r2 + 1, ansCol);
        if (!cell.getValue()) { cell.setValue(val); filled++; }
        usedRow[r2] = true;
        break;
      }
    }"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)

NEW = """    // [V12b] 1セルずつ読み書きするとサーバー往復が増えて遅いので、
    //   回答欄の列をまとめて読み、まとめて書き戻す。
    var col = sh.getRange(1, ansCol, last, 1).getValues();   // 読みは1回
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
    if (changed) sh.getRange(1, ansCol, last, 1).setValues(col);   // 書きも1回"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
