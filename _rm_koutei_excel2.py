# -*- coding: utf-8 -*-
"""[KOUTEI_EXCEL_REMOVE_V1] Excel版の工程管理表を撤去する（行指定）。

L2277 {/* [KOUTEI_XLSX_V1 …  から
L2362 付近の </span> まで（GAS_UI_V2 の直前）を削除。
見出し「🗂 工程管理表:」は GAS 側に付け直す。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_rmke2_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
L = io.open(P, encoding="utf-8").read().split("\n")

s_idx = None
for i, l in enumerate(L):
    if "KOUTEI_XLSX_V1 2026-10-29" in l:
        s_idx = i
        break
assert s_idx is not None, "開始が見つからない"

e_idx = None
for i, l in enumerate(L):
    if "KOUTEI_GAS_UI_V2 2026-10-29" in l:
        e_idx = i
        break
assert e_idx is not None and e_idx > s_idx, "終了が見つからない"

print("削除: L%d - L%d (%d行)" % (s_idx + 1, e_idx, e_idx - s_idx))

I = " " * (len(L[s_idx]) - len(L[s_idx].lstrip()))
# Excel版を消し、見出しだけ残す
NEW = [
    I + '{/* [KOUTEI_GAS_UI_V2 2026-10-29] 工程管理表はスプレッドシート方式に一本化。',
    I + '    Excel生成は書式を再現できないため撤去した。 */}',
    I + '<div className="w-full mt-2 pt-2 border-t border-slate-700/50">',
    I + '  <span className="text-base text-cyan-300 font-bold">🗂 工程管理表</span>',
    I + '</div>',
]
L[s_idx:e_idx] = NEW
io.open(P, "w", encoding="utf-8").write("\n".join(L))
print("削除しました")
