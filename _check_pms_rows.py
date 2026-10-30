# -*- coding: utf-8 -*-
"""PMS / スマートロック① / 必須確認③ の実際の項目名を確認する。"""
import io, json

t = io.open(r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts", encoding="utf-8").read()
defs = json.loads(t[t.index("= ") + 2:].strip())

for name in ["PMS", "\u30b9\u30de\u30fc\u30c8\u30ed\u30c3\u30af\u2460",
             "\u5fc5\u9808\u78ba\u8a8d\u2462"]:
    rows = defs.get(name)
    if not rows:
        continue
    ans = 0
    for r in rows[:6]:
        for c, v in enumerate(r):
            if "\u3054\u56de\u7b54\u6b04" in v:
                ans = c + 1
                break
        if ans:
            break
    print("\n=== %s (回答欄=%s) 先頭12行 ===" % (name, ans or "なし"))
    for ri, row in enumerate(rows[:12]):
        txt = [(c, v[:46]) for c, v in enumerate(row) if v]
        print("  %2d: %s" % (ri + 1, txt))
