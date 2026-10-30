# -*- coding: utf-8 -*-
"""全シートで自動入力できる項目を洗い出す。
ダッシュボードが持っているデータ(会社名/住所/担当者/電話/メーカー/台数/納期など)と
突き合わせて、どのシートのどの行に入れられるか一覧化する。
"""
import io, json

t = io.open(r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts", encoding="utf-8").read()
defs = json.loads(t[t.index("= ") + 2:].strip())

# ダッシュボードが持っている情報で埋められそうな語
KEYS = [
    "\u7d44\u7e54\u540d", "\u4f1a\u793e\u540d", "\u6cd5\u4eba\u540d",
    "\u7269\u4ef6\u540d", "\u5c4b\u53f7",
    "\u4f4f\u6240", "\u90f5\u4fbf\u756a\u53f7",
    "\u304a\u540d\u524d", "\u3054\u62c5\u5f53", "\u62c5\u5f53\u8005",
    "\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9",
    "\u96fb\u8a71\u756a\u53f7", "\u643a\u5e2f",
    "\u30e1\u30fc\u30ab\u30fc",
    "\u90e8\u5c4b\u306e\u7dcf\u6570", "\u5ba2\u5ba4\u6570", "\u7dcf\u5ba4\u6570",
    "\u7a3c\u50cd", "\u958b\u696d", "\u30aa\u30fc\u30d7\u30f3",
]

for sheet, rows in defs.items():
    # 回答欄の列
    ans = 0
    for r in rows[:6]:
        for c, v in enumerate(r):
            if "\u3054\u56de\u7b54\u6b04" in v:
                ans = c + 1
                break
        if ans:
            break
    hits = []
    for ri, row in enumerate(rows):
        txt = " ".join(row)
        for k in KEYS:
            if k in txt:
                label = max([x for x in row if x and x != "\u25a1"] or [""], key=len)
                hits.append((ri + 1, k, label[:38]))
                break
    if hits:
        print("\n=== %s (回答欄=%s列) ===" % (sheet, ans or "なし"))
        for ri, k, label in hits[:14]:
            print("  行%-4d [%s] %s" % (ri, k, label))
