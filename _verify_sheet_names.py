# -*- coding: utf-8 -*-
"""判定ロジックが出すシート名と、実際にDLされている雛形シート名を突き合わせる。
存在しないシートを指示すると Gemini が勝手に創作するため。"""
import io, glob, os, re

base = r"C:\Users\fyone\Downloads"
pat = os.path.join(base, "*" + "\u30d2\u30a2\u30ea\u30f3\u30b0" + "*.csv")
actual = []
for p in glob.glob(pat):
    n = os.path.basename(p)
    m = re.search(r" - (.+?)(?: \(\d+\))?\.csv$", n)
    if m:
        actual.append(m.group(1))
actual = sorted(set(actual))
print("=== 実在する雛形シート (%d) ===" % len(actual))
for a in actual:
    print("   ", a)

# page.tsx の hearingSheets ラベルを抽出
p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
s = io.open(p, encoding="utf-8").read()
i = s.index("const hearingSheets:")
j = s.index("\n                  ]", i)
blk = s[i:j]
labels = re.findall(r"label:\s*'([^']+)'", blk)
print("\n=== 判定が出すシート名 (%d) ===" % len(labels))
for l in labels:
    print("   ", l)

print("\n=== 突合 ===")
ng = 0
for l in labels:
    hit = [a for a in actual if a == l or a.replace("\u2460", "").replace("\u2461", "").replace("\u2462", "") == l]
    mark = "OK " if hit else "MISSING"
    if not hit:
        ng += 1
    print("  %-8s %s" % (mark, l))
print("\n実在シートのうち判定に出てこないもの:")
for a in actual:
    if a not in labels and "\u30d5\u30ed\u30fc\u30c1\u30e3\u30fc\u30c8" not in a:
        print("   (未使用)", a)
print("\nMISSING: %d" % ng)
