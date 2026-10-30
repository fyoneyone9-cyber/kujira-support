# -*- coding: utf-8 -*-
"""スマートロック②の18件のズレを調べる。"""
import io, csv, glob, os, json

p = [x for x in glob.glob(r"C:\Users\fyone\Downloads\*.csv")
     if "\u30b9\u30de\u30fc\u30c8\u30ed\u30c3\u30af\u2461" in os.path.basename(x)][0]
rows = list(csv.reader(io.open(p, encoding="utf-8-sig")))
print("=== 雛形CSV（先頭14行・列位置つき）===")
for i, r in enumerate(rows[:14]):
    cells = [(j, c.strip()[:40]) for j, c in enumerate(r) if c.strip()]
    print("%2d: %s" % (i + 1, cells))

t = io.open(r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts", encoding="utf-8").read()
defs = json.loads(t[t.index("= ") + 2:].strip())
d = defs["\u30b9\u30de\u30fc\u30c8\u30ed\u30c3\u30af\u2461"]
print("\n=== 定義側（先頭14行）===")
for i, r in enumerate(d[:14]):
    cells = [(j, c[:40]) for j, c in enumerate(r) if c]
    print("%2d: %s" % (i + 1, cells))
