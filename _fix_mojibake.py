# -*- coding: utf-8 -*-
"""[APPLICATION_PARSE_V8 2026-10-29] ソース内の日本語リテラル破損を修正。

発覚: blockRows(/担当者氏名/) が 0件。/担当者/ なら 7件。
  → route.ts に書いた「担当者氏名」の文字列が壊れていた。
     PowerShell 経由の編集で文字化けが混入したとみられる
     （MEMORY.md に記録済みの既知の罠。今回も踏んだ）。

対策: 日本語を含む正規表現を **\\uXXXX エスケープ**で書き直す。
  これなら編集経路に関係なく壊れない。
"""
import io, shutil, datetime, re

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\parse-application\route.ts"
shutil.copy2(P, P + ".bak_v8_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()


def esc(t):
    return "".join("\\u%04x" % ord(c) if ord(c) > 127 else c for c in t)


# 正規表現リテラルを置換（壊れている可能性のあるもの全部）
pairs = [
    ("blockRows(/\u62c5\u5f53\u8005\u6c0f\u540d/)", "blockRows(/" + esc("\u62c5\u5f53\u8005") + "/)"),
    ("blockValues(/\u5951\u7d04\u8005\u540d/)", "blockValues(/" + esc("\u5951\u7d04\u8005\u540d") + "/)"),
    ("blockValues(/^.{0,2}\u4f4f\u6240$/)", "blockValues(/^.{0,2}" + esc("\u4f4f\u6240") + "$/)"),
    ("blockValues(/\u8acb\u6c42\u66f8\u9001\u4ed8\u5148/)", "blockValues(/" + esc("\u8acb\u6c42\u66f8\u9001\u4ed8\u5148") + "/)"),
    ("blockValues(/\u8a2d\u7f6e\u5148\u65bd\u8a2d\u540d\u79f0/)", "blockValues(/" + esc("\u8a2d\u7f6e\u5148\u65bd\u8a2d\u540d\u79f0") + "/)"),
    ("blockValues(/\u8a2d\u7f6e\u5148\u65bd\u8a2d\u4f4f\u6240/)", "blockValues(/" + esc("\u8a2d\u7f6e\u5148\u65bd\u8a2d\u4f4f\u6240") + "/)"),
    ("labeledValue(/\u62c5\u5f53\u8005\u6c0f\u540d/", "labeledValue(/" + esc("\u62c5\u5f53\u8005") + "/"),
    ("labeledValue(/^.{0,2}\u9023\u7d61\u5148$/", "labeledValue(/^.{0,2}" + esc("\u9023\u7d61\u5148") + "$/"),
    ("blockRows(/\u7d0d\u54c1\u5e0c\u671b\u65e5/)", "blockRows(/" + esc("\u7d0d\u54c1\u5e0c\u671b\u65e5") + "/)"),
]
for a, b in pairs:
    n = s.count(a)
    if n:
        s = s.replace(a, b)
    print("  %-40s %d箇所" % (a[:40], n))

# 文字列比較も同様に
s = s.replace('/^(TEL|FAX|\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9|\u3012)$/',
              '/^(TEL|FAX|' + esc("\u30e1\u30fc\u30eb\u30a2\u30c9\u30ec\u30b9") + '|' + esc("\u3012") + ')$/')
s = s.replace("/^(\u54c1\u540d|\u5c0f\u8a08|\u6d88\u8cbb\u7a0e|\u5408\u8a08|\u203b)/",
              "/^(" + esc("\u54c1\u540d|\u5c0f\u8a08|\u6d88\u8cbb\u7a0e|\u5408\u8a08|\u203b") + ")/")
s = s.replace("/\u30eb\u30fc\u30e0\u5229\u7528\u6599/", "/" + esc("\u30eb\u30fc\u30e0\u5229\u7528\u6599") + "/")

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
