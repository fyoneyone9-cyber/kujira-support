# -*- coding: utf-8 -*-
"""[HEARING_SHEET_DEFS_V4 2026-10-29] 雛形の構造を完全に保持して抽出する。

雛形(必須確認①)の実構造:
  A列 = 大見出し(1. 物件で利用する『鍵』について) / 説明文 / 5.その他の設問
  B列 = 設問(インデント1段)
  D列 = 設問(インデント2段。決済手段の4項目)
  L列 = ご回答欄(TRUE/FALSE)
  N,O,P列 = 社内用(〜のヒアリングシートへ / タブレットの場合不要 / 田中社長にご連絡)

V3の不具合: 社内用列を削除したあと「行末の空セルを落とす」処理で、
            L列より右が消えるのは良いが、列の詰め直しはしていなかったため
            見た目は合っていた。しかし全シート取り込めていなかった。
V4: 対象を「ヒアリングシート」CSVに限定しつつ、重複(1)ファイルを除外。
    列位置は完全保持。社内用列のみ空文字化(削除せず位置を維持)する。
"""
import io, os, csv, glob, re, json

BASE = r"C:\Users\fyone\Downloads"
PREFIX = "\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8"
FLOW = "\uff08\u793e\u5185\u7528\uff09\u30d5\u30ed\u30fc\u30c1\u30e3\u30fc\u30c8"

INTERNAL_MARK = [
    "\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8\u3078",
    "DMS\u5165\u529b\u9805\u76ee",
    "\u30bf\u30d6\u30ec\u30c3\u30c8\u306e\u5834\u5408\u4e0d\u8981",
    "\u793e\u5185\u7528",
    "\u7530\u4e2d\u793e\u9577",
    "\u55b6\u696d\u306b\u78ba\u8a8d",
    "\u30af\u30e9\u30a4\u30a2\u30f3\u30c8",
    "\u7269\u4ef6\u4e00\u89a7",
    "\u975e\u8868\u793a\u306b\u3057\u3066",
]


def load(path):
    for enc in ("utf-8-sig", "cp932", "utf-8"):
        try:
            return list(csv.reader(io.open(path, encoding=enc)))
        except Exception:
            continue
    return []


def extract(path):
    rows = load(path)
    if not rows:
        return []
    ncol = max(len(r) for r in rows)
    # 社内用の列を特定
    bad = set()
    for c in range(ncol):
        col = [(r[c] if c < len(r) else "") for r in rows]
        if any(m in " ".join(col) for m in INTERNAL_MARK):
            bad.add(c)
    keep = [c for c in range(ncol) if c not in bad]

    out = []
    for r in rows:
        line = []
        for c in keep:
            v = r[c].strip() if c < len(r) else ""
            if v in ("TRUE", "FALSE"):
                v = "\u25a1"
            line.append(v)
        while line and line[-1] == "":
            line.pop()
        if not any(line):
            continue
        out.append(line)
    return out


defs = {}
for p in sorted(glob.glob(os.path.join(BASE, "*.csv"))):
    fn = os.path.basename(p)
    if not fn.startswith(PREFIX):
        continue
    if re.search(r" \(\d+\)\.csv$", fn):      # 重複DLファイルは無視
        continue
    m = re.search(r" - (.+?)\.csv$", fn)
    if not m:
        continue
    name = m.group(1)
    if name == FLOW:
        continue
    # 「（後日作成）」等の注記を落として正式なシート名にする
    clean = re.sub(r"\uff08[^\uff09]*\uff09$", "", name).strip()
    defs[clean] = extract(p)

print("sheets: %d" % len(defs))
for k in sorted(defs):
    v = defs[k]
    print("  %-20s rows=%-4d maxcol=%d" % (k, len(v), max((len(r) for r in v), default=0)))

OUT = r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts"
f = io.open(OUT, "w", encoding="utf-8")
f.write("// [HEARING_SHEET_DEFS_V4 2026-10-29] 自動生成 (_rebuild_v4.py)\n")
f.write("// 雛形スプレッドシートを『列位置を保ったまま』抽出。\n")
f.write("//   A列=大見出し/説明文, B列=設問, D列=設問(2段目), L列=ご回答欄(□)\n")
f.write("// 社内用の列(〜のヒアリングシートへ / タブレットの場合不要 等)は列ごと除去。\n")
f.write("// ⚠ 手で編集しないこと。雛形が変わったら _rebuild_v4.py を再実行する。\n")
f.write("export const HEARING_SHEET_DEFS: Record<string, string[][]> = ")
f.write(json.dumps(defs, ensure_ascii=False, indent=1))
f.write("\n")
f.close()
print("\nwrote", OUT)
