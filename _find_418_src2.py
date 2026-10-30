# -*- coding: utf-8 -*-
"""時刻から算出した変数が、描画で使われているかを追う。
days / hoursAgo / diff / level などが SSR/CSR で変わると #418 になる。
"""
import io, re

p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
L = io.open(p, encoding="utf-8").read().split("\n")

# 1) 時刻から算出している変数名を集める
vars_ = {}
for i, l in enumerate(L, 1):
    m = re.search(r"const\s+(\w+)\s*=.*(Date\.now\(\)|new Date\(\))", l)
    if m:
        vars_[m.group(1)] = i
print("=== 時刻から算出される変数 ===")
for v, i in vars_.items():
    print("  L%-5d %s" % (i, v))

# 2) それらが JSX で描画されているか
print("\n=== 描画に使われている箇所 ===")
for i, l in enumerate(L, 1):
    s = l.strip()
    if "<" not in s and not s.startswith("{"):
        continue
    for v in vars_:
        if re.search(r"\{[^}]*\b" + re.escape(v) + r"\b", s):
            print("L%-5d [%s] %s" % (i, v, s[:130]))
            break

# 3) 関数から返る日数系
print("\n=== daysUntil / level 等の計算関数 ===")
for i, l in enumerate(L, 1):
    if re.search(r"(function|const)\s+\w*(days|level|alert|diff)\w*\s*=", l, re.I) and "Date" in l:
        print("L%-5d %s" % (i, l.strip()[:130]))
