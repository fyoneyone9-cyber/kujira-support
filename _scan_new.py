# -*- coding: utf-8 -*-
"""新しいヒアリングシート構成を調べる。"""
import io, csv, glob, os, re

BASE = r"C:\Users\fyone\Downloads"
COPY = "\u30b3\u30d4\u30fc"   # 「コピー 〜」で始まる新しい方
hits = [p for p in glob.glob(os.path.join(BASE, "*.csv"))
        if os.path.basename(p).startswith(COPY)]
print("新構成のCSV: %d枚\n" % len(hits))

names = []
for p in sorted(hits):
    m = re.search(r" - (.+?)\.csv$", os.path.basename(p))
    if m:
        names.append((m.group(1).strip(), p))

for n, p in names:
    rows = None
    for enc in ("utf-8-sig", "cp932", "utf-8"):
        try:
            rows = list(csv.reader(io.open(p, encoding=enc)))
            break
        except Exception:
            continue
    print("=== %s  (%d行) ===" % (n, len(rows) if rows else 0))

print("\n--- 必須確認①が657バイトと小さい。中身を確認 ---")
for n, p in names:
    if n.startswith("\u5fc5\u9808\u78ba\u8a8d\u2460"):
        rows = list(csv.reader(io.open(p, encoding="utf-8-sig")))
        for i, r in enumerate(rows):
            cells = [(j, c.strip()[:40]) for j, c in enumerate(r) if c.strip()]
            print("  %2d: %s" % (i + 1, cells))
