# -*- coding: utf-8 -*-
"""PayPay利用申請の件名・本文を全文出力する。"""
import io, csv, glob, os

p = [x for x in glob.glob(r"C:\Users\fyone\Downloads\*.csv")
     if "PayPay" in os.path.basename(x)][0]
rows = list(csv.reader(io.open(p, encoding="utf-8-sig")))
print("=== 件名 (row12 B) ===")
print(rows[11][1])
print("\n=== 本文 (row13 B) 全文 ===")
print(rows[12][1])
print("\n=== 宛先情報 ===")
print("TO:", rows[3][1] if len(rows[3]) > 1 else "")
print("CC候補:")
for i in range(4, 11):
    if len(rows[i]) > 3 and rows[i][3].strip():
        label = rows[i][1].strip() if len(rows[i]) > 1 else ""
        print("   %-14s %s" % (label, rows[i][3].strip()))
