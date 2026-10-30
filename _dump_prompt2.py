# -*- coding: utf-8 -*-
import io
p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
L = io.open(p, encoding="utf-8").read().split("\n")
for i in range(1393, 1460):
    print("%5d| %s" % (i, L[i - 1]))
