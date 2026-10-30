# -*- coding: utf-8 -*-
import io
p = r"C:\Users\fyone\Downloads" + "\\" + "\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8\uff08\u3072\u306a\u5f62\u30fb\u95b2\u89a7\u7528\uff09 - \u5fc5\u9808\u78ba\u8a8d\u2460.csv"
print(io.open(p, encoding="utf-8-sig").read())
