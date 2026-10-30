# -*- coding: utf-8 -*-
import io
p = r"C:\GensparkClaw\kujira-support\src\components\Sidebar.tsx"
L = io.open(p, encoding="utf-8").read().split("\n")
for a, b in [(1, 40), (55, 70), (105, 135)]:
    print("===== L%d-%d =====" % (a, b))
    for i in range(a, min(b, len(L) + 1)):
        print("%4d| %s" % (i, L[i - 1].rstrip()[:140]))
    print()
