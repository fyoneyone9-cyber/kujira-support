# -*- coding: utf-8 -*-
"""雛形CSVの生の姿を、列位置つきで正確にダンプする。
Excelの見え方と比較するため、空セルも含めて表示する。
"""
import io, csv

SRC = (r"C:\Users\fyone\Downloads"
       "\\\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8\uff08\u3072\u306a\u5f62\u30fb\u95b2\u89a7\u7528\uff09"
       " - \u5fc5\u9808\u78ba\u8a8d\u2460.csv")
rows = list(csv.reader(io.open(SRC, encoding="utf-8-sig")))
print("rows=%d" % len(rows))
cols = max(len(r) for r in rows)
print("cols=%d\n" % cols)

def colname(i):
    return chr(65 + i) if i < 26 else chr(64 + i // 26) + chr(65 + i % 26)

for i, r in enumerate(rows):
    parts = []
    for j, c in enumerate(r):
        v = c.strip().replace("\n", "\\n")
        if v:
            parts.append("%s=%s" % (colname(j), v[:46]))
    print("%2d| %s" % (i + 1, " ; ".join(parts) if parts else "(空行)"))
