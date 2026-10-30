# -*- coding: utf-8 -*-
"""React #418 = ハイドレーション不一致(text content mismatch)。
サーバーとクライアントで異なる値を描画している箇所を探す。
典型: Date.now() / new Date().toLocaleString() / Math.random()
"""
import io, re

p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
L = io.open(p, encoding="utf-8").read().split("\n")
pat = re.compile(r"Date\.now\(\)|new Date\(\)|toLocaleString|toLocaleDateString|Math\.random")
for i, l in enumerate(L, 1):
    if pat.search(l):
        print("%5d| %s" % (i, l.strip()[:150]))
