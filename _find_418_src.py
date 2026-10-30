# -*- coding: utf-8 -*-
"""React #418 = text content mismatch。
SSR と CSR で異なるテキストを出す箇所を、JSX描画部に絞って洗い出す。
対象: 時刻依存 / localStorage / window / random
"""
import io, re

p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
src = io.open(p, encoding="utf-8").read()
L = src.split("\n")

RISK = [
    ("Date.now", r"Date\.now\(\)"),
    ("new Date()", r"new Date\(\)"),
    ("toLocale", r"toLocale\w*\("),
    ("localStorage", r"localStorage"),
    ("window.", r"\bwindow\."),
    ("Math.random", r"Math\.random"),
]

print("=== 描画に直結しそうな箇所（JSXの { } 内）===")
for i, l in enumerate(L, 1):
    s = l.strip()
    # JSX っぽい行: {xxx} を含み、かつ < or > がある、または単独の { 式 }
    in_jsx = bool(re.search(r"\{[^{}]*\}", s)) and (s.startswith("{") or "<" in s)
    if not in_jsx:
        continue
    for name, pat in RISK:
        if re.search(pat, s):
            print("%5d| [%s] %s" % (i, name, s[:140]))
            break

print("\n=== useState の初期値に危険な値（SSRとCSRで変わる）===")
for i, l in enumerate(L, 1):
    if "useState(" in l:
        for name, pat in RISK:
            if re.search(pat, l):
                print("%5d| [%s] %s" % (i, name, l.strip()[:140]))
                break
