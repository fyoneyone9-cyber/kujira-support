# -*- coding: utf-8 -*-
"""[HEARING_SHEET_DEFS_V1 2026-10-29]
DL済みの実シートCSVから「お客様に見せる設問」だけを抽出し、
page.tsx に埋め込むための TypeScript 定義ファイルを生成する。

社内用の列は必ず落とす:
 - 必須確認②の1行目に「↓ここは社内用の情報欄なので、お客様送付時には非表示にしてください」
 - 「〜のヒアリングシートへ」の誘導列、「DMS入力項目」列、「タブレットの場合不要」注記列
"""
import io, os, csv, glob, re, json

BASE = r"C:\Users\fyone\Downloads"
FLOW = "\uff08\u793e\u5185\u7528\uff09\u30d5\u30ed\u30fc\u30c1\u30e3\u30fc\u30c8"

# 社内用と判断する語（セル値に含まれていたらその列は捨てる）
INTERNAL_MARK = [
    "\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8\u3078",   # 〜のヒアリングシートへ
    "DMS\u5165\u529b\u9805\u76ee",                              # DMS入力項目
    "\u30bf\u30d6\u30ec\u30c3\u30c8\u306e\u5834\u5408\u4e0d\u8981",  # タブレットの場合不要
    "\u793e\u5185\u7528",                                        # 社内用
    "\u7530\u4e2d\u793e\u9577",                                  # 田中社長にご連絡
    "\u55b6\u696d\u306b\u78ba\u8a8d",                            # 営業に確認
    "\u30af\u30e9\u30a4\u30a2\u30f3\u30c8",                      # クライアント一覧
    "\u7269\u4ef6\u4e00\u89a7",                                  # 物件一覧
]

def load(path):
    for enc in ("utf-8-sig", "cp932", "utf-8"):
        try:
            return list(csv.reader(io.open(path, encoding=enc)))
        except Exception:
            continue
    return []

def internal_cols(rows):
    """社内用と判定される列インデックスの集合"""
    bad = set()
    ncol = max((len(r) for r in rows), default=0)
    for c in range(ncol):
        col = [(r[c] if c < len(r) else "") for r in rows]
        joined = " ".join(col)
        if any(m in joined for m in INTERNAL_MARK):
            bad.add(c)
    return bad

def extract(path):
    rows = load(path)
    if not rows:
        return []
    bad = internal_cols(rows)
    out = []
    for r in rows:
        cells = [(c if c else "") for i, c in enumerate(r) if i not in bad]
        line = [c.strip() for c in cells if c.strip()]
        if not line:
            continue
        # TRUE/FALSE のみの行は回答欄なので記号化
        line = ["\u25a1" if x in ("FALSE", "TRUE") else x for x in line]
        out.append(line)
    return out

defs = {}
for p in sorted(glob.glob(os.path.join(BASE, "*.csv"))):
    m = re.search(r" - (.+?)(?: \(\d+\))?\.csv$", os.path.basename(p))
    if not m:
        continue
    name = m.group(1)
    if name == FLOW or name in defs:
        continue
    defs[name] = extract(p)

print("extracted sheets:", len(defs))
for k, v in defs.items():
    print("  %-18s rows=%d" % (k, len(v)))

out = io.open(r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts", "w", encoding="utf-8")
out.write("// [HEARING_SHEET_DEFS_V1 2026-10-29] 自動生成 (_build_sheet_defs.py)\n")
out.write("// 雛形スプレッドシートの各シートから『お客様に見せる設問』だけを抽出したもの。\n")
out.write("// 社内用の列（DMS入力項目 / 〜のヒアリングシートへ / タブレットの場合不要 等）は除去済み。\n")
out.write("// ⚠ 手で編集しないこと。雛形が変わったら _build_sheet_defs.py を再実行する。\n")
out.write("export const HEARING_SHEET_DEFS: Record<string, string[][]> = ")
out.write(json.dumps(defs, ensure_ascii=False, indent=1))
out.write("\n")
out.close()
print("\nwrote src/lib/hearingSheetDefs.ts")
