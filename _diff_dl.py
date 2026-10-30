# -*- coding: utf-8 -*-
"""21:39版と21:42版(1)の差分を確認する。シート構成が変わっていないか。"""
import io, glob, os, re, hashlib

BASE = r"C:\Users\fyone\Downloads"
old, new = {}, {}
for p in glob.glob(os.path.join(BASE, "*.csv")):
    fn = os.path.basename(p)
    if not fn.startswith("\u30b3\u30d4\u30fc"):
        continue
    m = re.search(r" - (.+?)(?: \(1\))?\.csv$", fn)
    if not m:
        continue
    name = m.group(1).strip()
    h = hashlib.md5(io.open(p, "rb").read()).hexdigest()[:8]
    if " (1).csv" in fn:
        new[name] = h
    else:
        old[name] = h

print("21:39版: %d枚 / 21:42版: %d枚\n" % (len(old), len(new)))

allk = sorted(set(old) | set(new))
for k in allk:
    o, n = old.get(k), new.get(k)
    if o and n:
        s = "同一" if o == n else "★内容が変わった"
    elif o:
        s = "★21:42版に無い（削除された？）"
    else:
        s = "★21:42版で追加"
    print("  %-20s %s" % (k, s))
