# -*- coding: utf-8 -*-
"""[HYDRATION_FIX_V2] days21 表示に mounted ガードを付ける（行指定版）。
絵文字の表記揺れで文字列一致が使えないため、行番号で処理する。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_418c_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
L = io.open(P, encoding="utf-8").read().split("\n")

done = 0
for i, l in enumerate(L):
    if "days21" not in l:
        continue
    st = l.strip()
    # JSX の描画行だけが対象（{val === null && ... で始まるもの）
    if st.startswith("{val === null &&") and "<span" in st:
        indent = l[:len(l) - len(l.lstrip())]
        L[i] = indent + st.replace("{val === null &&", "{mounted && val === null &&", 1)
        print("patched L%d: %s" % (i + 1, L[i].strip()[:110]))
        done += 1

assert done >= 1, "対象行が見つからない"
io.open(P, "w", encoding="utf-8").write("\n".join(L))
print("total patched:", done)
