# -*- coding: utf-8 -*-
"""[HEARING_GAS_V11b 2026-10-29] Surface は明示的にプリンタON。

指示:「サーフェスはON」
  Surface はプリンタを接続できるので、タブレット語を含む記載があっても
  Surface があれば優先してONにする。
  （例: equipment に「Surface用スタンド」と「タブレット」が混在するケース対策）
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_printsf_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                                      const isTabletTerminal = equipItems.some(e => {
                                        const t = (e.name || '') + ' ' + (e.value || '')
                                        if (/ルームタブレット|room.?tablet/i.test(t)) return false
                                        return /タブレット|tablet/i.test(t)
                                      })
                                      if (hasPrinter || !isTabletTerminal) equips.push('printer')"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)

NEW = """                                      //   Surface / KIOSK はプリンタ接続可なので、タブレット語があってもON優先。
                                      const hasSurfaceOrKiosk = equipItems.some(e =>
                                        /surface|KIOSK|キオスク|卓上/i.test((e.name || '') + ' ' + (e.value || '')))
                                      const isTabletTerminal = equipItems.some(e => {
                                        const t = (e.name || '') + ' ' + (e.value || '')
                                        if (/ルームタブレット|room.?tablet/i.test(t)) return false
                                        return /タブレット|tablet/i.test(t)
                                      })
                                      if (hasPrinter || hasSurfaceOrKiosk || !isTabletTerminal) equips.push('printer')"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
