# -*- coding: utf-8 -*-
"""PayPay利用申請テンプレートの構造を確認する。"""
import io, csv, glob, os

hits = [p for p in glob.glob(r"C:\Users\fyone\Downloads\*.csv")
        if "PayPay" in os.path.basename(p) and "\u30c6\u30f3\u30d7\u30ec" in os.path.basename(p)]
if not hits:
    hits = [p for p in glob.glob(r"C:\Users\fyone\Downloads\*.csv")
            if "PayPay\u5229\u7528\u7533\u8acb" in os.path.basename(p)]
print("files:", [os.path.basename(p) for p in hits])
if not hits:
    raise SystemExit(0)

p = hits[0]
for enc in ("utf-8-sig", "cp932", "utf-8"):
    try:
        rows = list(csv.reader(io.open(p, encoding=enc)))
        print("enc:", enc)
        break
    except Exception:
        continue

print("rows=%d cols=%d\n" % (len(rows), max(len(r) for r in rows)))

def cn(i):
    return chr(65 + i) if i < 26 else chr(64 + i // 26) + chr(65 + i % 26)

for i, r in enumerate(rows):
    parts = [("%s=%s" % (cn(j), c.strip().replace("\n", "\\n")[:60]))
             for j, c in enumerate(r) if c.strip()]
    print("%3d| %s" % (i + 1, " ; ".join(parts)[:260] if parts else "(空行)"))
