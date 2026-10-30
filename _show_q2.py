# -*- coding: utf-8 -*-
import io, csv, glob, os
base = r"C:\Users\fyone\Downloads"
p = os.path.join(base, "\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8\uff08\u3072\u306a\u5f62\u30fb\u95b2\u89a7\u7528\uff09 - \u5fc5\u9808\u78ba\u8a8d\u2461.csv")
rows = list(csv.reader(io.open(p, encoding="utf-8-sig")))
print("rows:", len(rows), "maxcol:", max(len(r) for r in rows))
for i, r in enumerate(rows[:40]):
    cells = [(j, c) for j, c in enumerate(r) if c.strip()]
    print(i, cells)
