# -*- coding: utf-8 -*-
"""[HEARING_SHEET_DEFS_V6 2026-10-29] 社内用列の誤判定を修正。

重大バグ: スマートロック②で設問本文(C列)が消え、社内用のP列が残っていた。
  雛形 7行目: C列「ログインアカウント ⇨ …」 / O列「ロック設定」 / P列「ログインID」
  定義 7行目: P列「ログインID」だけ

原因: 社内用マーカーの判定が『列全体を連結した文字列に含まれるか』だったため、
      設問本文に "DMS" 等が出てくる列まで社内用と誤判定していた。
      さらに P列(ログインID等)は社内用マーカーを含まないので残っていた。

対策:
  ・社内用の判定は「その列のヘッダ付近(先頭6行)にマーカーがあるか」で行う
  ・『↓ここは社内用の情報欄』が書かれている列から右は全て社内用とする
    （雛形の設計どおり。N列以降が社内用ゾーン）
"""
import io, os, csv, glob, re, json

BASE = r"C:\Users\fyone\Downloads"
PREFIX = "\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8"
FLOW = "\uff08\u793e\u5185\u7528\uff09\u30d5\u30ed\u30fc\u30c1\u30e3\u30fc\u30c8"

# この文字が現れた列から右は社内用ゾーン
ZONE_MARK = "\u793e\u5185\u7528\u306e\u60c5\u5831\u6b04"      # 社内用の情報欄
# 単独で社内用と判断する列ヘッダ
HEAD_MARK = ["DMS\u5165\u529b\u9805\u76ee", "\u30af\u30e9\u30a4\u30a2\u30f3\u30c8", "\u7269\u4ef6\u4e00\u89a7"]
# セル単位で消す（列は消さない）
CELL_MARK = ["\u306e\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8\u3078",
             "\u7530\u4e2d\u793e\u9577", "\u55b6\u696d\u306b\u78ba\u8a8d",
             "\u30bf\u30d6\u30ec\u30c3\u30c8\u306e\u5834\u5408\u4e0d\u8981"]


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

    # (1) 「社内用の情報欄」が書かれた列を探す → そこから右は全部社内用
    zone_start = None
    for r in rows[:8]:
        for c, v in enumerate(r):
            if ZONE_MARK in v:
                zone_start = c
                break
        if zone_start is not None:
            break

    bad = set()
    if zone_start is not None:
        for c in range(zone_start, ncol):
            bad.add(c)
    # (2) ヘッダに DMS入力項目 等がある列も社内用
    for c in range(ncol):
        head = " ".join((r[c] if c < len(r) else "") for r in rows[:6])
        if any(m in head for m in HEAD_MARK):
            bad.add(c)

    out = []
    for r in rows:
        line = []
        for c in range(ncol):
            v = r[c].strip() if c < len(r) else ""
            if c in bad:
                v = ""
            elif any(m in v for m in CELL_MARK):
                v = ""                       # セル単位で除去（列は保持）
            if v in ("TRUE", "FALSE"):
                v = "\u25a1"
            line.append(v)
        while line and line[-1] == "":
            line.pop()
        out.append(line)
    while out and not any(out[-1]):
        out.pop()
    return out


defs = {}
for p in sorted(glob.glob(os.path.join(BASE, "*.csv"))):
    fn = os.path.basename(p)
    if not fn.startswith(PREFIX) or re.search(r" \(\d+\)\.csv$", fn):
        continue
    m = re.search(r" - (.+?)\.csv$", fn)
    if not m:
        continue
    name = m.group(1)
    if name == FLOW:
        continue
    clean = re.sub(r"\uff08[^\uff09]*\uff09$", "", name).strip()
    d = extract(p)
    if len(d) >= 2:
        defs[clean] = d

print("sheets: %d" % len(defs))
for k in sorted(defs):
    print("  %-20s rows=%d" % (k, len(defs[k])))

OUT = r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts"
f = io.open(OUT, "w", encoding="utf-8")
f.write("// [HEARING_SHEET_DEFS_V6 2026-10-29] 自動生成 (_fix_internal_detect.py)\n")
f.write("// 『社内用の情報欄』が書かれた列から右を社内用ゾーンとして除去する。\n")
f.write("// 設問本文の列を誤って消さないよう、判定はヘッダ付近のみで行う。\n")
f.write("export const HEARING_SHEET_DEFS: Record<string, string[][]> = ")
f.write(json.dumps(defs, ensure_ascii=False, indent=1))
f.write("\n")
f.close()
print("\nwrote", OUT)
