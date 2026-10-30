# -*- coding: utf-8 -*-
"""[KOUTEI_EXCEL_REMOVE_V1 2026-10-29] 工程管理表のExcel版を撤去する。

指摘:「📥 工程管理表を作成 / 📄 原本を開く これいらない スプシのみ」
  スプレッドシート方式に一本化する。
  Excel生成はレイアウトを再現できないので役目を終えた。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_rmkexcel_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
L = io.open(P, encoding="utf-8").read().split("\n")

# 「📥 工程管理表を作成」ボタン〜「※ 使わない機材の…」までを削除
start = None
for i, l in enumerate(L):
    if "KOUTEI_XLSX_V1 2026-10-29] 工程管理表" in l:
        start = i
        break
assert start is not None, "開始位置が見つからない"

end = None
for i in range(start, min(start + 80, len(L))):
    if "使わない機材の工程行を自動で削除します" in l if False else "使わない機材の工程行を自動で削除します" in L[i]:
        # その次の </span> まで
        j = i
        while "</span>" not in L[j]:
            j += 1
        end = j + 1
        break
assert end is not None, "終了位置が見つからない"

print("削除範囲: L%d - L%d (%d行)" % (start + 1, end, end - start))
for n in range(start, min(start + 4, end)):
    print("   %s" % L[n].strip()[:80])
print("   ...")
for n in range(max(start, end - 3), end):
    print("   %s" % L[n].strip()[:80])

# 見出し行だけ残す（🗂 工程管理表: のラベル）
indent = len(L[start]) - len(L[start].lstrip())
L[start:end] = []

io.open(P, "w", encoding="utf-8").write("\n".join(L))
print("\n削除しました")
