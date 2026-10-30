# -*- coding: utf-8 -*-
import io, re
p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
L = io.open(p, encoding="utf-8").read().split("\n")
print("=== ltWarnings.push / cardAlerts.push ===")
for i, l in enumerate(L, 1):
    if re.search(r"(ltWarnings|cardAlerts)\.push", l):
        print("%5d| %s" % (i, l.strip()[:175]))
print("\n=== ltWarnings 描画部 ===")
for i in range(1058, 1100):
    print("%5d| %s" % (i, L[i - 1].rstrip()[:175]))
