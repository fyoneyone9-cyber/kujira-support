# -*- coding: utf-8 -*-
"""[ENCODING_AUDIT_V1 2026-10-29] 文字化けを検出する。

本日3回、日本語リテラルの破損で機能が死んだ。
破損パターン: 正常な日本語の中に U+E000〜U+F8FF(私用領域) や
  不自然な「E」「チE」「老E」などが混ざる。

判定: 日本語文字列の中に以下があれば疑う
  ・私用領域の文字
  ・ひらがな/カタカナ/漢字の直後に単独の大文字ラテン（E等）が来る
"""
import io, re, glob, os

TARGETS = [
    r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js",
    r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html",
    r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx",
    r"C:\GensparkClaw\kujira-support\src\app\api\delivery\hearing-xlsx\route.ts",
    r"C:\GensparkClaw\kujira-support\src\app\api\delivery\koutei-xlsx\route.ts",
    r"C:\GensparkClaw\kujira-support\src\app\api\delivery\parse-application\route.ts",
]

# 日本語の直後に単独ラテン大文字が来る（典型的な化け）
PAT = re.compile(r"[ぁ-んァ-ヶ一-龥][A-Z](?![A-Za-z0-9])")
PUA = re.compile(r"[\ue000-\uf8ff]")

total = 0
for p in TARGETS:
    if not os.path.exists(p):
        continue
    lines = io.open(p, encoding="utf-8").read().split("\n")
    hits = []
    for i, l in enumerate(lines, 1):
        if PUA.search(l):
            hits.append((i, "私用領域", l.strip()[:70]))
        elif PAT.search(l):
            hits.append((i, "日本語+大文字", l.strip()[:70]))
    if hits:
        print("\n=== %s ===" % os.path.basename(p))
        for n, kind, txt in hits[:12]:
            print("  L%-5d [%s] %s" % (n, kind, txt))
        if len(hits) > 12:
            print("  ... 他 %d件" % (len(hits) - 12))
    total += len(hits)

print("\n疑わしい箇所の合計: %d" % total)
