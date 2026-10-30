# -*- coding: utf-8 -*-
import io, glob, csv
hits = glob.glob(r"C:\Users\fyone\Downloads\*" + "\u30d2\u30a2\u30ea\u30f3\u30b0" + "*.csv")
for p in hits:
    print("=== FILE:", p)
    for enc in ("utf-8-sig", "cp932", "utf-8"):
        try:
            t = io.open(p, encoding=enc).read()
            print("--- encoding:", enc, "len:", len(t))
            print(t)
            break
        except Exception as e:
            print("  fail", enc, e)
