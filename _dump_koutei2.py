# -*- coding: utf-8 -*-
"""工程管理表の構造を確認する（ファイル名はglobで部分一致）。"""
import io, csv, glob, os

hits = [p for p in glob.glob(r"C:\Users\fyone\Downloads\*.csv")
        if "\u5de5\u7a0b\u7ba1\u7406" in os.path.basename(p)]
print("files:", [os.path.basename(p) for p in hits])
if not hits:
    raise SystemExit(0)

p = hits[0]
rows = None
for enc in ("utf-8-sig", "cp932", "utf-8"):
    try:
        rows = list(csv.reader(io.open(p, encoding=enc)))
        print("encoding:", enc)
        break
    except Exception:
        continue

print("rows=%d cols=%d\n" % (len(rows), max(len(r) for r in rows)))

def cn(i):
    return chr(65 + i) if i < 26 else chr(64 + i // 26) + chr(65 + i % 26)

for i, r in enumerate(rows[:70]):
    parts = [("%s=%s" % (cn(j), c.strip().replace("\n", "\\n")[:30]))
             for j, c in enumerate(r) if c.strip()]
    print("%3d| %s" % (i + 1, " ; ".join(parts)[:190] if parts else "(空行)"))
