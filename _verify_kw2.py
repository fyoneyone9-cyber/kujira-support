# -*- coding: utf-8 -*-
"""[ENCODING_AUDIT_V2] キーワード(\\uXXXXエスケープ)と実シート名の対応を検証する。"""
import io, json, re, codecs

t = io.open(r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts", encoding="utf-8").read()
defs = json.loads(t[t.index("= ") + 2:].strip())

g = io.open(r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js", encoding="utf-8").read()
blk = g[g.index("var EQUIP_KEYWORDS"):g.index("var ALWAYS_KEYWORDS")]

kw = {}
for m in re.finditer(r"(\w+):\s*\[([^\]]+)\]", blk):
    words = []
    for x in m.group(2).split(","):
        x = x.strip().strip("'")
        if not x:
            continue
        # \uXXXX を実文字に戻す
        words.append(codecs.decode(x, "unicode_escape") if "\\u" in x else x)
    kw[m.group(1)] = words

ab = g[g.index("var ALWAYS_KEYWORDS"):]
ab = ab[:ab.index("]")]
always = [codecs.decode(x.strip().strip("'"), "unicode_escape")
          for x in re.findall(r"'([^']+)'", ab)]

print("ALWAYS:", always)
print("\n=== 実シート名 -> 判定キー ===")
bad = []
for name in sorted(defs):
    hit = []
    if any(a in name for a in always):
        hit.append("ALWAYS")
    for k, words in kw.items():
        if any(w in name for w in words):
            hit.append(k)
    if not hit:
        bad.append(name)
    print("  %-20s %s" % (name, " / ".join(hit) if hit else "NG 拾えない"))

print("\n拾えないシート:", bad if bad else "なし ← 正常")
unused = [k for k, w in kw.items() if not any(any(x in n for x in w) for n in defs)]
print("未使用のキー:", unused if unused else "なし ← 正常")
