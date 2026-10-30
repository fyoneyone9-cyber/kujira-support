# -*- coding: utf-8 -*-
"""自動入力すべきセルを特定する。
必須確認②には「組織名(会社名)」「物件名」「物件の住所」「郵便番号」等があり、
回答欄に案件情報を入れられる。
"""
import io, json

t = io.open(r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts", encoding="utf-8").read()
defs = json.loads(t[t.index("= ") + 2:].strip())

KEYS = ["\u7d44\u7e54\u540d", "\u7269\u4ef6\u540d", "\u4f4f\u6240", "\u90f5\u4fbf\u756a\u53f7",
        "\u304a\u540d\u524d", "\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9", "\u96fb\u8a71\u756a\u53f7",
        "\u90e8\u5c4b\u306e\u7dcf\u6570", "\u30e1\u30fc\u30ab\u30fc"]

for sheet, rows in defs.items():
    hit = []
    for ri, row in enumerate(rows):
        for ci, c in enumerate(row):
            if any(k in c for k in KEYS) and len(c) < 60:
                hit.append((ri, ci, c[:40]))
    if hit:
        print("\n=== %s ===" % sheet)
        for ri, ci, c in hit[:12]:
            # 同じ行の回答欄位置を探す
            ans = [j for j, v in enumerate(rows[ri]) if v == "\u25a1"]
            print("  行%-3d 列%-2d %-40s 回答欄列=%s" % (ri, ci, c, ans))
