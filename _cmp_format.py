# -*- coding: utf-8 -*-
"""正しい雛形CSVと、hearingSheetDefs.ts の中身を比較する。"""
import io, csv, json, re

SRC = (r"C:\Users\fyone\Downloads"
       "\\\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8\uff08\u3072\u306a\u5f62\u30fb\u95b2\u89a7\u7528\uff09"
       " - \u5fc5\u9808\u78ba\u8a8d\u2460.csv")

rows = list(csv.reader(io.open(SRC, encoding="utf-8-sig")))
print("=== 正しいCSV: %d行 / 最大%d列 ===" % (len(rows), max(len(r) for r in rows)))
for i, r in enumerate(rows[:14]):
    cells = [(j, c) for j, c in enumerate(r) if c.strip()]
    print("%2d: %s" % (i, cells))

# 生成側
t = io.open(r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts", encoding="utf-8").read()
defs = json.loads(t[t.index("= ") + 2:].strip())
d = defs["\u5fc5\u9808\u78ba\u8a8d\u2460"]
print("\n=== 現在の定義: %d行 ===" % len(d))
for i, r in enumerate(d[:14]):
    print("%2d: %s" % (i, r))
