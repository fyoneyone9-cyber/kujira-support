# -*- coding: utf-8 -*-
"""フローチャートCSVに登場する「〜のヒアリングシートへ」の遷移先名を全部抜く。
= 雛形に存在するはずのシート名の正解リスト。"""
import io, os, re

base = r"C:\Users\fyone\Downloads"
f = os.path.join(base, "\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8\uff08\u3072\u306a\u5f62\u30fb\u95b2\u89a7\u7528\uff09 - \uff08\u793e\u5185\u7528\uff09\u30d5\u30ed\u30fc\u30c1\u30e3\u30fc\u30c8.csv")
t = io.open(f, encoding="utf-8-sig").read()
names = set()
for m in re.finditer(r"([^,\"\n]+?)\u306e\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8\u3078", t):
    names.add(m.group(1).strip())
print("=== フローチャートが指す遷移先シート ===")
for n in sorted(names):
    print("   ", n)

# 必須確認①の誘導列も
g = os.path.join(base, "\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8\uff08\u3072\u306a\u5f62\u30fb\u95b2\u89a7\u7528\uff09 - \u5fc5\u9808\u78ba\u8a8d\u2460.csv")
t2 = io.open(g, encoding="utf-8-sig").read()
names2 = set()
for m in re.finditer(r"([^,\"\n]+?)\u306e\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8\u3078", t2):
    names2.add(m.group(1).strip())
print("\n=== 必須確認①が指す遷移先シート ===")
for n in sorted(names2):
    print("   ", n)

print("\n=== 和集合（雛形に存在すべきシート） ===")
for n in sorted(names | names2):
    print("   ", n)
