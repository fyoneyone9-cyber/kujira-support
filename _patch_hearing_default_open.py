# -*- coding: utf-8 -*-
"""[HEARING_DEFAULT_OPEN_V1 2026-10-29]
ヒアリングシート欄を「未登録のときはデフォルトで展開」する。

現状: openSections[key] が undefined だと常に閉じている。
対策: 作業員欄(L2056)と同じ `?? 既定値` 方式にする。
      既定値 = 「URL未登録 かつ スキップ指定なし」= 要対応なので開く。
      登録済み/スキップ済みなら閉じたまま（画面を汚さない）。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_hopen_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
L = io.open(P, encoding="utf-8").read().split("\n")

# 1494行目: ▲閉じる / ▼開く の表示
i = 1494
assert "openSections[`hearing_${it.id}`]" in L[i - 1], "L1494 mismatch: %r" % L[i - 1][:90]
L[i - 1] = L[i - 1].replace(
    "openSections[`hearing_${it.id}`] ?",
    "(openSections[`hearing_${it.id}`] ?? hearingDefaultOpen) ?", 1)
print("L1494 ->", L[i - 1].strip()[:110])

# 1496行目: 本体の表示条件
j = 1496
assert "openSections[`hearing_${it.id}`] &&" in L[j - 1], "L1496 mismatch: %r" % L[j - 1][:90]
L[j - 1] = L[j - 1].replace(
    "{openSections[`hearing_${it.id}`] &&",
    "{(openSections[`hearing_${it.id}`] ?? hearingDefaultOpen) &&", 1)
print("L1496 ->", L[j - 1].strip()[:110])

# hearingSkip 定義の直後に既定値を追加
k = None
for n, l in enumerate(L):
    if "const hearingSkip = it.dashboard_todos?.['hearing_sheet_url_skip']" in l:
        k = n
        break
assert k is not None, "hearingSkip not found"
indent = L[k][:len(L[k]) - len(L[k].lstrip())]
L.insert(k + 1, indent + "// [HEARING_DEFAULT_OPEN_V1 2026-10-29] 未登録(=要対応)なら既定で展開する。\n"
         + indent + "//   登録済み/スキップ済みなら閉じたままにして画面を汚さない。\n"
         + indent + "const hearingDefaultOpen = !hearingUrl && !hearingSkip")
print("inserted default at L%d" % (k + 2))

io.open(P, "w", encoding="utf-8").write("\n".join(L))
print("patched OK")
