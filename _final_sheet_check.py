# -*- coding: utf-8 -*-
"""DLされた実シートと、フローチャートが参照するシート名を最終突合する。"""
import io, glob, os, re

base = r"C:\Users\fyone\Downloads"
actual = set()
for p in glob.glob(os.path.join(base, "*.csv")):
    n = os.path.basename(p)
    m = re.search(r" - (.+?)(?: \(\d+\))?\.csv$", n)
    if m:
        actual.add(m.group(1))
flow = "\uff08\u793e\u5185\u7528\uff09\u30d5\u30ed\u30fc\u30c1\u30e3\u30fc\u30c8"
sheets = sorted(a for a in actual if a != flow)

print("=== DL済みの実シート (%d枚) ===" % len(sheets))
for a in sheets:
    p = glob.glob(os.path.join(base, "* - " + a + ".csv"))
    size = os.path.getsize(p[0]) if p else 0
    print("   %-20s %6d bytes" % (a, size))

# フローが参照する名前
f = os.path.join(base, "\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8\uff08\u3072\u306a\u5f62\u30fb\u95b2\u89a7\u7528\uff09 - " + flow + ".csv")
t = io.open(f, encoding="utf-8-sig").read()
ref = set()
for m in re.finditer(r"([^,\"\n]+?)\u306e\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8\u3078", t):
    ref.add(m.group(1).strip())

print("\n=== フローが参照するが、実ファイルが無いシート ===")
miss = sorted(r for r in ref if r not in actual and r != "\u30b9\u30de\u30fc\u30c8\u30ed\u30c3\u30af")
for r in miss:
    print("   ", r)
print("\n（スマートロックは ①② として実在）")
print("\n実在:%d  参照:%d  不足:%d" % (len(sheets), len(ref), len(miss)))
