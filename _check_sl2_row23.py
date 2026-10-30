# -*- coding: utf-8 -*-
"""スマートロック②23行目の差分を確認する。"""
import io, csv, glob, os, json

p = [x for x in glob.glob(r"C:\Users\fyone\Downloads\*.csv")
     if "\u30b9\u30de\u30fc\u30c8\u30ed\u30c3\u30af\u2461" in os.path.basename(x)][0]
rows = list(csv.reader(io.open(p, encoding="utf-8-sig")))
print("=== 雛形 21-26行 ===")
for i in range(20, min(26, len(rows))):
    cells = [(j, c.strip()[:46]) for j, c in enumerate(rows[i]) if c.strip()]
    print("%2d: %s" % (i + 1, cells))

t = io.open(r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts", encoding="utf-8").read()
defs = json.loads(t[t.index("= ") + 2:].strip())
d = defs["\u30b9\u30de\u30fc\u30c8\u30ed\u30c3\u30af\u2461"]
print("\n=== 定義 21-26行 ===")
for i in range(20, min(26, len(d))):
    cells = [(j, c[:46]) for j, c in enumerate(d[i]) if c]
    print("%2d: %s" % (i + 1, cells))
