# -*- coding: utf-8 -*-
import io
P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
s = io.open(P, encoding="utf-8").read()
i = s.find("dialog.html")
L = s[:i].count("\n") + 1
lines = s.split("\n")
for n in range(L - 22, L + 6):
    if 0 <= n < len(lines):
        print("%5d| %s" % (n + 1, lines[n].rstrip()[:120]))
