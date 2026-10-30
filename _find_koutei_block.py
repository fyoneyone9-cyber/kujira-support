# -*- coding: utf-8 -*-
"""工程管理のGASブロックの正確な範囲を特定する。"""
import io

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
L = io.open(P, encoding="utf-8").read().split("\n")

mark = "KOUTEI_GAS_UI_V1"
start = None
for i, l in enumerate(L):
    if mark in l:
        start = i
        break
print("start = L%d" % (start + 1))

# インデントの深さで閉じ </div> を探す
indent = len(L[start]) - len(L[start].lstrip())
print("indent =", indent)
for i in range(start, min(start + 60, len(L))):
    cur = len(L[i]) - len(L[i].lstrip()) if L[i].strip() else -1
    print("%5d|%3d| %s" % (i + 1, cur, L[i][:110]))
