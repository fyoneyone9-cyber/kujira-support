# -*- coding: utf-8 -*-
"""工程管理表のC列（区分）を全部洗い出し、機材との対応を確認する。"""
import io, csv, glob, os, collections

p = [x for x in glob.glob(r"C:\Users\fyone\Downloads\*.csv")
     if "\u5de5\u7a0b\u7ba1\u7406" in os.path.basename(x)][0]
rows = list(csv.reader(io.open(p, encoding="utf-8-sig")))

cnt = collections.Counter()
for r in rows[3:]:
    if len(r) > 2 and r[2].strip():
        cnt[r[2].strip()] += 1

print("=== C列(区分)の一覧 ===")
for k, v in sorted(cnt.items()):
    print("  %-28s %d行" % (k, v))

print("\n=== B列(品目) ===")
b = collections.Counter()
for r in rows[3:]:
    if len(r) > 1 and r[1].strip():
        b[r[1].strip()] += 1
for k, v in b.most_common():
    print("  %-20s %d行" % (k, v))

print("\n総行数:", len(rows))
