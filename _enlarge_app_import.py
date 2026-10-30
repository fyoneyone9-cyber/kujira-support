# -*- coding: utf-8 -*-
"""[APPLICATION_IMPORT_V2 2026-10-29] 申込書取り込み欄の文字を大きくする。

指摘:「小さすぎ」
  text-xs(12px) で書いていた。本文は text-base(16px)、
  注釈も text-sm(14px) まで上げる。ボタンも押しやすく。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_appsize_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

start = s.index("{/* [APPLICATION_IMPORT_V1 2026-10-29] 申込書(.xlsx)の取り込み。")
end = s.index("{/* [CLIENT_EMAIL_V1 2026-10-29] お客様メールアドレス。")
seg = s[start:end]
before = seg

# 見出し・ボタン
seg = seg.replace(
    'className="text-sm text-indigo-300 font-bold"',
    'className="text-base text-indigo-300 font-bold"')
seg = seg.replace(
    'className="text-sm px-2.5 py-1 rounded bg-indigo-700 hover:bg-indigo-600 text-white font-bold cursor-pointer transition-colors"',
    'className="text-base px-4 py-2 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-bold cursor-pointer transition-colors shadow"')
# 取込済バッジ
seg = seg.replace(
    'className="text-xs text-emerald-400"',
    'className="text-sm text-emerald-400 font-bold"')
# 取り込んだ内容の表示
seg = seg.replace(
    'className="mt-1.5 text-xs text-slate-300 flex flex-wrap gap-x-3 gap-y-0.5"',
    'className="mt-2 text-sm text-slate-200 flex flex-wrap gap-x-4 gap-y-1 font-medium"')
# 注釈
seg = seg.replace(
    'className="text-xs text-slate-500 mt-1"',
    'className="text-sm text-slate-400 mt-1.5"')
# 枠も少し広く
seg = seg.replace(
    'rounded-lg px-2.5 py-2"',
    'rounded-lg px-3 py-2.5"')

assert seg != before, "置換が効いていない"
s = s[:start] + seg + s[end:]
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
