# -*- coding: utf-8 -*-
import io
p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
L = io.open(p, encoding="utf-8").read().split("\n")
for a, b in [(540, 585), (1095, 1135)]:
    print("===== %d-%d =====" % (a, b))
    for i in range(a, b):
        print("%d|%s" % (i, L[i - 1]))
