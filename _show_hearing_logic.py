# -*- coding: utf-8 -*-
import io, re
p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
L = io.open(p, encoding="utf-8").read().split("\n")
hit = []
for i, l in enumerate(L, 1):
    if re.search(r"\u5fc5\u9808\u78ba\u8a8d|\u30d2\u30a2\u30ea\u30f3\u30b0|hearing|joinLabel|hasP400|Gemini|\u96db\u5f62", l):
        hit.append(i)
# 近接行をまとめて表示
shown = set()
for i in hit:
    for j in range(max(1, i - 2), min(len(L), i + 3)):
        if j not in shown:
            shown.add(j)
for j in sorted(shown):
    print("%5d| %s" % (j, L[j - 1][:190]))
