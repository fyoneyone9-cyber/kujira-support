# -*- coding: utf-8 -*-
import io, re
p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
s = io.open(p, encoding="utf-8").read()
L = s.split("\n")
# Geminiプロンプト生成部を探す
for i, l in enumerate(L, 1):
    if "Gemini" in l:
        print("%5d| %s" % (i, l.strip()[:200]))
