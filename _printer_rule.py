# -*- coding: utf-8 -*-
"""[HEARING_GAS_V11 2026-10-29] プリンタは「タブレット以外」ならONにする。

指示:「プリンタはタブレット以外 ON」
  チェックイン端末がタブレットの場合はプリンタを繋げないため不要。
  KIOSK / 卓上KIOSK / Surface なら必要。

実データ(400件)の調査:
  タブレット 74件 / Surface 36件 / 卓上 1件 / プリンタ 10件
  equipment は [{name, value}] の配列。name に「タブレット」等が入る。

判定:
  端末がタブレット(ルームタブレットを除く)なら OFF、それ以外は ON。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_printer_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                                      if (hasPrinter) equips.push('printer')"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)

NEW = """                                      // [HEARING_GAS_V11 2026-10-29] プリンタは「タブレット以外」ならON。
                                      //   チェックイン端末がタブレットだとプリンタを接続できないため。
                                      //   ※ルームタブレットは客室用なので端末種別とは無関係 → 除外して判定する
                                      const isTabletTerminal = equipItems.some(e => {
                                        const t = (e.name || '') + ' ' + (e.value || '')
                                        if (/ルームタブレット|room.?tablet/i.test(t)) return false
                                        return /タブレット|tablet/i.test(t)
                                      })
                                      if (hasPrinter || !isTabletTerminal) equips.push('printer')"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
