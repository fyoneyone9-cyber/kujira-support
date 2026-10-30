# -*- coding: utf-8 -*-
import io
P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
L = io.open(P, encoding="utf-8").read().split("\n")
for key in ["my_koutei_url", "my_sheet_url"]:
    print("\n===== %s =====" % key)
    hits = [i for i, l in enumerate(L) if key in l]
    if not hits:
        print("  見つからない")
        continue
    a = min(hits) - 6
    b = max(hits) + 8
    for i in range(max(0, a), min(len(L), b)):
        print("%5d| %s" % (i + 1, L[i][:130]))
