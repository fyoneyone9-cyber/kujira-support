# -*- coding: utf-8 -*-
"""[HYDRATION_FIX_V3] サイドバーの時計もマウント後に描画する。"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\components\Sidebar.tsx"
bak = P + ".bak_clock_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
L = io.open(P, encoding="utf-8").read().split("\n")

print("--- L112-145 ---")
for i in range(112, 146):
    if i <= len(L):
        print("%4d| %s" % (i, L[i - 1].rstrip()[:140]))
