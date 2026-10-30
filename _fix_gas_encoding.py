# -*- coding: utf-8 -*-
"""[HEARING_GAS_V21 2026-10-29] GASファイルの日本語リテラル破損を根治する。

発覚: EQUIP_KEYWORDS の日本語が壊れていた。
    '現釁E'  <- 現金
    '端末カーチE' <- 端末カード
    '工亁E'  <- 工事
  これではシート名と照合できず、判定が機能しない。

原因: PowerShell 経由の編集で文字化けが混入（本日3回目）。

根治: キーワードを **\\uXXXX エスケープ**で書く。
  編集経路に関係なく壊れないし、目視でも壊れたら気づける。
"""
import io, shutil, datetime, re

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
shutil.copy2(P, P + ".bak_enc_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()


def esc(t):
    return "".join("\\u%04x" % ord(c) if ord(c) > 127 else c for c in t)


KW = [
    ("pms",        ["PMS"]),
    ("smartlock",  ["\u30b9\u30de\u30fc\u30c8\u30ed\u30c3\u30af"]),          # スマートロック
    ("cardkey",    ["\u30ab\u30fc\u30c9\u30ad\u30fc"]),                       # カードキー
    ("cylinder",   ["\u30b7\u30ea\u30f3\u30c0\u30fc"]),                       # シリンダー
    ("cash",       ["\u73fe\u91d1"]),                                         # 現金
    ("p400",       ["\u7aef\u672b\u30ab\u30fc\u30c9"]),                       # 端末カード
    ("sumaho",     ["\u30b9\u30de\u30db\u30ab\u30fc\u30c9", "\u30b9\u30de\u30fc\u30c8\u30ab\u30fc\u30c9"]),
    ("paypay",     ["PayPay", "\u30da\u30a4\u30da\u30a4"]),                   # ペイペイ
    ("printer",    ["\u30d7\u30ea\u30f3\u30bf"]),                             # プリンタ
    ("roomtablet", ["\u30eb\u30fc\u30e0\u30bf\u30d6\u30ec\u30c3\u30c8"]),     # ルームタブレット
    ("precheckin", ["\u4e8b\u524d\u30c1\u30a7\u30c3\u30af\u30a4\u30f3"]),     # 事前チェックイン
    ("koji",       ["\u5de5\u4e8b"]),                                         # 工事
]
lines = ["var EQUIP_KEYWORDS = {"]
for k, ws in KW:
    vals = ", ".join("'%s'" % esc(w) for w in ws)
    lines.append("  %-12s [%s]," % (k + ":", vals))
lines.append("};")
NEW_KW = "\n".join(lines)

i = s.index("var EQUIP_KEYWORDS = {")
j = s.index("};", i) + 2
s = s[:i] + NEW_KW + s[j:]

# ALWAYS_KEYWORDS も同様に
i2 = s.index("var ALWAYS_KEYWORDS = [")
j2 = s.index("];", i2) + 2
s = s[:i2] + ("var ALWAYS_KEYWORDS = ['%s', '%s'];"
              % (esc("\u5fc5\u9808\u78ba\u8a8d"), esc("\u8868\u7d19"))) + s[j2:]

io.open(P, "w", encoding="utf-8").write(s)
print("EQUIP_KEYWORDS / ALWAYS_KEYWORDS をエスケープ表記に置換")

# 検証
t = io.open(P, encoding="utf-8").read()
m = re.search(r"var EQUIP_KEYWORDS.*?\};", t, re.S)
print("\n" + m.group(0))
