# -*- coding: utf-8 -*-
"""React #418 の残り原因を探す。
JSXの中（描画される箇所）で時刻依存の値を出しているところだけを抽出する。
"""
import io, re

p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
L = io.open(p, encoding="utf-8").read().split("\n")
pat = re.compile(r"toLocaleString|toLocaleDateString|toLocaleTimeString|Date\.now\(\)|new Date\(\)")
for i, l in enumerate(L, 1):
    if not pat.search(l):
        continue
    # JSX内（{ } で囲まれて描画されている）かどうかの粗い判定
    jsx = bool(re.search(r"\{[^}]*(toLocale|Date\.now)", l)) and ("<" in l or ">" in l or l.strip().startswith("{"))
    mark = "JSX" if jsx else "   "
    print("%s %5d| %s" % (mark, i, l.strip()[:150]))
