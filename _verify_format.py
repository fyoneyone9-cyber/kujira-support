# -*- coding: utf-8 -*-
"""列位置が保たれたか、正しいCSVと生成定義を突き合わせる。"""
import io, csv, json

SRC = (r"C:\Users\fyone\Downloads"
       "\\\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8\uff08\u3072\u306a\u5f62\u30fb\u95b2\u89a7\u7528\uff09"
       " - \u5fc5\u9808\u78ba\u8a8d\u2460.csv")
rows = list(csv.reader(io.open(SRC, encoding="utf-8-sig")))

t = io.open(r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts", encoding="utf-8").read()
defs = json.loads(t[t.index("= ") + 2:].strip())
d = defs["\u5fc5\u9808\u78ba\u8a8d\u2460"]

print("=== 比較: 設問がどの列にあるか ===")
print("%-4s %-10s %s" % ("行", "正(列)", "生成(列)"))
# 「現在、「スマートロック」を…」の行で確認
key = "\u30b9\u30de\u30fc\u30c8\u30ed\u30c3\u30af\u300d\u3092\u3054\u5229\u7528"
for i, r in enumerate(rows):
    if any(key in c for c in r):
        col_src = [j for j, c in enumerate(r) if key in c][0]
        ans_src = [j for j, c in enumerate(r) if c in ("TRUE", "FALSE")]
        print("正しいCSV : 設問=列%d / 回答欄=列%s" % (col_src, ans_src))
        break
for r in d:
    if any(key in c for c in r):
        col_g = [j for j, c in enumerate(r) if key in c][0]
        ans_g = [j for j, c in enumerate(r) if c == "\u25a1"]
        print("生成定義   : 設問=列%d / 回答欄=列%s" % (col_g, ans_g))
        break

print("\n=== 生成定義 先頭10行（列位置つき）===")
for i, r in enumerate(d[:10]):
    cells = [(j, c[:40]) for j, c in enumerate(r) if c]
    print("%2d: %s" % (i, cells))
