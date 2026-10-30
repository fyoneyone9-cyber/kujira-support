# -*- coding: utf-8 -*-
"""[HEARING_SHEET_DEFS_V7 2026-10-29] 新構成(14シート)で定義を作り直す。

変更点:
  必須確認① 32行 -> 8行に縮小
  スマートロック② 廃止、③ が新設
  「工事」「スマホカード決済」が追加
  PayPay決済 / ルームタブレット / フロントチェックイン / デイユース / 補助金 は廃止

ファイル名が「コピー 〜」で始まるものが新構成。古いCSVと混ざらないよう明示的に選ぶ。
"""
import io, os, csv, glob, re, json

BASE = r"C:\Users\fyone\Downloads"
COPY = "\u30b3\u30d4\u30fc"

ZONE_MARK = "\u793e\u5185\u7528\u306e\u60c5\u5831\u6b04"
HEAD_MARK = ["DMS\u5165\u529b\u9805\u76ee", "\u30af\u30e9\u30a4\u30a2\u30f3\u30c8", "\u7269\u4ef6\u4e00\u89a7"]
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
    zone = None
    for r in rows[:8]:
        for c, v in enumerate(r):
            if ZONE_MARK in v:
                zone = c
                break
        if zone is not None:
            break
    bad = set()
    if zone is not None:
        for c in range(zone, ncol):
            bad.add(c)
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
                v = ""
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
    if not fn.startswith(COPY):
        continue
    if re.search(r" \(\d+\)\.csv$", fn):
        continue
    m = re.search(r" - (.+?)\.csv$", fn)
    if not m:
        continue
    name = m.group(1).strip()
    d = extract(p)
    if len(d) >= 2:
        defs[name] = d

print("sheets: %d" % len(defs))
for k in sorted(defs):
    print("  %-20s rows=%d" % (k, len(defs[k])))

OUT = r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts"
f = io.open(OUT, "w", encoding="utf-8")
f.write("// [HEARING_SHEET_DEFS_V7 2026-10-29] 自動生成 (_rebuild_v7.py)\n")
f.write("// 雛形の構成変更に追従。必須確認①が8行に縮小、スマートロック③と工事が新設。\n")
f.write("// 『社内用の情報欄』が書かれた列から右は除去する。\n")
f.write("export const HEARING_SHEET_DEFS: Record<string, string[][]> = ")
f.write(json.dumps(defs, ensure_ascii=False, indent=1))
f.write("\n")
f.close()
print("\nwrote", OUT)
