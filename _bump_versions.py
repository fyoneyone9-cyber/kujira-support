# -*- coding: utf-8 -*-
"""[VERSION_BUMP] 4ファイルのバージョンを揃える。
ヒアリング = V27 / 工程管理 = K2
片方だけ古い事故を防ぐため、必ずこのスクリプトでまとめて上げること。
"""
import io, re

PAIRS = [
    (r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js", "GAS_VERSION", "V27 2026-10-29"),
    (r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html", "DIALOG_VERSION", "V27 2026-10-29"),
    (r"C:\GensparkClaw\kujira-support\public\docs\koutei-gas.js", "KOUTEI_VERSION", "K2 2026-10-29"),
    (r"C:\GensparkClaw\kujira-support\public\docs\koutei-gas-dialog.html", "DIALOG_VERSION", "K2 2026-10-29"),
]
import os
for p, var, ver in PAIRS:
    s = io.open(p, encoding="utf-8").read()
    s2 = re.sub(r"var %s = '[^']*';" % var, "var %s = '%s';" % (var, ver), s, count=1)
    assert s2 != s, "置換失敗: %s %s" % (os.path.basename(p), var)
    io.open(p, "w", encoding="utf-8").write(s2)
    print("  %-30s %s = %s" % (os.path.basename(p), var, ver))

# 検証
print("\n=== 照合 ===")
def getv(p, var):
    t = io.open(p, encoding="utf-8").read()
    m = re.search(r"var %s = '([^']*)'" % var, t)
    return m.group(1) if m else None

h1 = getv(PAIRS[0][0], "GAS_VERSION")
h2 = getv(PAIRS[1][0], "DIALOG_VERSION")
k1 = getv(PAIRS[2][0], "KOUTEI_VERSION")
k2 = getv(PAIRS[3][0], "DIALOG_VERSION")
print("  ヒアリング: %s / %s -> %s" % (h1, h2, "一致" if h1 == h2 else "不一致!!"))
print("  工程管理  : %s / %s -> %s" % (k1, k2, "一致" if k1 == k2 else "不一致!!"))
