# -*- coding: utf-8 -*-
"""カードキーシートで重複が残る理由を調べる。"""
import io, json

t = io.open(r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts", encoding="utf-8").read()
defs = json.loads(t[t.index("= ") + 2:].strip())
d = defs["\u30ab\u30fc\u30c9\u30ad\u30fc"]
print("rows:", len(d))
for i, r in enumerate(d[:14]):
    cells = [(j, c[:34]) for j, c in enumerate(r) if c]
    print("%2d: %s" % (i, cells))
