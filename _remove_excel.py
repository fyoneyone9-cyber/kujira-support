# -*- coding: utf-8 -*-
"""[HEARING_CLEANUP_V1 2026-10-29] Excel生成を撤去し、Apps Script方式に一本化する。

指摘:「エクセルもういらない」「📋設定をコピーがマニュアルにない」

やること:
  (1) 「📥 Excelで作成」「📁 Googleドライブ」「🤖 Gemini用プロンプト」ボタンを削除
  (2) 添付の説明文から「Excelで作成」への言及を削除
  (3) 手順の冒頭に「📋 設定をコピー」を明記（⓪として既にあるが場所が分かりにくい）
"""
import io, shutil, datetime, re

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_rmexcel_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# (1) Excel作成ボタン〜Googleドライブ〜注記までを削除
start = s.index("                              {/* [HEARING_XLSX_V1 2026-10-29] Gemini")
end_mark = "\u203b Excel\u3092\u30c9\u30e9\u30a4\u30d6\u306b\u30c9\u30e9\u30c3\u30b0 \u2192 \u53f3\u30af\u30ea\u30c3\u30af\u300cGoogle\u30b9\u30d7\u30ec\u30c3\u30c9\u30b7\u30fc\u30c8\u3067\u958b\u304f\u300d"
e = s.index(end_mark)
end = s.index("</span>", e) + len("</span>")
removed = s[start:end]
s = s[:start] + s[end:]
print("removed %d chars (Excel/Drive/Gemini block)" % len(removed))

# (2) 添付の説明文を修正
OLD2 = "\u203b \u6dfb\u4ed8\u3059\u308b\u3082\u306e: \u2460\u4e0a\u306e\u300c\ud83d\udce5 Excel\u3067\u4f5c\u6210\u300d\u306e\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8 \u2461\u300c\ud83d\udcce \u8a2d\u7f6e\u6e96\u5099PDF\u300d"
if s.count(OLD2) == 1:
    NEW2 = "\u203b \u6dfb\u4ed8\u3059\u308b\u3082\u306e: \u2460\u4e0a\u3067\u4f5c\u6210\u3057\u305f\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8 \u2461\u300c\ud83d\udcce \u8a2d\u7f6e\u6e96\u5099PDF\u300d"
    s = s.replace(OLD2, NEW2, 1)
    print("添付説明を修正")

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
