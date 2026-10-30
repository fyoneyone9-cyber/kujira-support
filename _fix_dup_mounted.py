# -*- coding: utf-8 -*-
"""mounted は既に L413 で宣言済みだった。私が追加した重複分(L427付近)を削除する。"""
import io

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
L = io.open(P, encoding="utf-8").read().split("\n")

print("--- L410-432 ---")
for i in range(410, 433):
    print("%5d| %s" % (i, L[i - 1].rstrip()[:130]))

# 私が足したブロック(コメント3行 + useState + useEffect)を探して消す
mark = "[HYDRATION_FIX_V1 2026-10-29] \u6642\u523b\u8868\u793a\u306fSSR"
idx = None
for i, l in enumerate(L):
    if mark in l:
        idx = i
        break
if idx is None:
    print("\n追加ブロックが見つからない")
else:
    # コメント3行 + useState + useEffect の計5行を削除
    seg = L[idx:idx + 5]
    print("\n削除対象:")
    for x in seg:
        print("   ", x.strip()[:110])
    del L[idx:idx + 5]
    io.open(P, "w", encoding="utf-8").write("\n".join(L))
    print("\nremoved 5 lines")
