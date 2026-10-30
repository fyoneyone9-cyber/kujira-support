# -*- coding: utf-8 -*-
import io, glob, os
pat = r"C:\Users\fyone\Downloads\*" + "\u30d2\u30a2\u30ea\u30f3\u30b0" + "*.csv"
for p in sorted(glob.glob(pat)):
    print("\n\n########## FILE:", os.path.basename(p), os.path.getsize(p), "bytes")
    for enc in ("utf-8-sig", "cp932", "utf-8"):
        try:
            t = io.open(p, encoding=enc).read()
            print(t)
            break
        except Exception:
            continue
