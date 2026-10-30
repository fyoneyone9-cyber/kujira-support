# -*- coding: utf-8 -*-
"""キーワードが実シート名を全てカバーできるか検証する。"""
import io, json, re

t = io.open(r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts", encoding="utf-8").read()
defs = json.loads(t[t.index("= ") + 2:].strip())

g = io.open(r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js", encoding="utf-8").read()
blk = g[g.index("var EQUIP_KEYWORDS"):g.index("var ALWAYS_KEYWORDS")]
kw = {}
for m in re.finditer(r"(\w+):\s*\[([^\]]+)\]", blk):
    kw[m.group(1)] = [x.strip().strip("'") for x in m.group(2).split(",")]

always = ["\u5fc5\u9808\u78ba\u8a8d", "\u8868\u7d19"]

print("=== 実シート名 -> どのキーで拾えるか ===")
uncovered = []
for name in sorted(defs):
    hit = []
    if any(a in name for a in always):
        hit.append("ALWAYS")
    for k, words in kw.items():
        if any(w in name for w in words):
            hit.append(k)
    if not hit:
        uncovered.append(name)
    print("  %-20s %s" % (name, " / ".join(hit) if hit else "❌ 拾えない"))

print("\n拾えないシート:", uncovered if uncovered else "なし ← 正常")

print("\n=== 未使用のキー（対応シートが無い）===")
unused = []
for k, words in kw.items():
    if not any(any(w in n for w in words) for n in defs):
        unused.append(k)
print(" ", unused if unused else "なし ← 正常")
