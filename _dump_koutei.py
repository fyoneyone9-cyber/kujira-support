# -*- coding: utf-8 -*-
"""工程管理表の構造を確認する。"""
import io, csv, glob, os

hits = glob.glob(r"C:\Users\fyone\Downloads\*\u5de5\u7a0b\u7ba1\u7406*.csv")
for p in hits:
    print("FILE:", os.path.basename(p), os.path.getsize(p))
if not hits:
    print("not found")
    raise SystemExit(0)

rows = None
for enc in ("utf-8-sig", "cp932", "utf-8"):
    try:
        rows = list(csv.reader(io.open(hits[0], encoding=enc)))
        print("encoding:", enc)
        break
    except Exception:
        continue

print("rows=%d cols=%d\n" % (len(rows), max(len(r) for r in rows)))

def cn(i):
    return chr(65 + i) if i < 26 else chr(64 + i // 26) + chr(65 + i % 26)

for i, r in enumerate(rows[:60]):
    parts = [("%s=%s" % (cn(j), c.strip().replace("\n", "\\n")[:34]))
             for j, c in enumerate(r) if c.strip()]
    print("%3d| %s" % (i + 1, " ; ".join(parts) if parts else "(空行)"))
