# -*- coding: utf-8 -*-
"""[HEARING_UI_SIZE_V1 2026-10-29] 文字が小さすぎて読めない問題の修正。

要望:「小さすぎてわかんねえ」

対象: ヒアリングシート欄に追加した各ブロック（設置手順/送付メール/工程管理表）。
      text-[11px] は見出しの注釈用サイズで、本文に使うには小さすぎた。
      手順本文は text-sm(14px)、ボタンは text-xs(12px) 以上にする。
"""
import io, shutil, datetime, re

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_size_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# 今回追加したブロックの範囲を特定（Excel作成ボタン〜工程管理表の終わりまで）
start = s.index("{/* [HEARING_XLSX_V1 2026-10-29] Gemini")
end = s.index("\u203b \u4f7f\u308f\u306a\u3044\u6a5f\u6750\u306e\u5de5\u7a0b\u884c\u3092\u81ea\u52d5\u3067\u524a\u9664\u3057\u307e\u3059")
seg = s[start:end + 400]
orig = seg

# サイズを上げる
seg = seg.replace('text-[11px]', 'text-sm')
seg = seg.replace('text-[10px]', 'text-xs')
# 手順番号の丸を大きく
seg = seg.replace('w-5 h-5 rounded-full', 'w-6 h-6 rounded-full')
# 既存の text-xs ボタンは text-sm に
seg = seg.replace('text-xs rounded-lg font-bold', 'text-sm rounded-lg font-bold')
# 行間を広げる
seg = seg.replace('space-y-1.5 text-sm', 'space-y-3 text-sm')
seg = seg.replace('px-2 py-0.5 rounded bg-', 'px-2.5 py-1 rounded bg-')

s = s[:start] + seg + s[end + 400:]
io.open(P, "w", encoding="utf-8").write(s)
print("replaced %d chars -> %d" % (len(orig), len(seg)))
