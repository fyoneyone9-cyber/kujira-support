# -*- coding: utf-8 -*-
import io
p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
L = io.open(p, encoding="utf-8").read().split("\n")
for i in range(770, 812):
    print("%5d| %s" % (i, L[i - 1].rstrip()[:160]))
