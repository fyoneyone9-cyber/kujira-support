# -*- coding: utf-8 -*-
"""[HEARING_SHEET_DEFS_V5 2026-10-29] 行を削除せず、雛形と完全に同じ行構成にする。

判明した問題:
 (1) 社内用の「↓ここは社内用の情報欄なので…」行(2行目)を丸ごと消していたため、
     3行目以降が全部1行ずつ上にズレていた。
     → 行は消さず、社内用の『列』だけを空にする。行数を雛形と一致させる。
 (2) スマートロック②・フロントチェックインが空(2行)になっていた。
     Downloadsに該当CSVが無いため。存在するものだけ定義に入れる。
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
    bad = set()
    for c in range(ncol):
        col = [(r[c] if c < len(r) else "") for r in rows]
        if any(m in " ".join(col) for m in INTERNAL_MARK):
            bad.add(c)

    out = []
    for r in rows:
        line = []
        for c in range(ncol):
            v = r[c].strip() if c < len(r) else ""
            if c in bad:
                v = ""                       # 社内用の列は空にする（列は残す）
            if v in ("TRUE", "FALSE"):
                v = "\u25a1"
            line.append(v)
        while line and line[-1] == "":
            line.pop()
        out.append(line)                     # 空行も残す（行番号を雛形と合わせる）
    # 末尾の完全な空行だけ落とす
    while out and not any(out[-1]):
        out.pop()
    return out


defs = {}
for p in sorted(glob.glob(os.path.join(BASE, "*.csv"))):
    fn = os.path.basename(p)
    if not fn.startswith(PREFIX):
        continue
    if re.search(r" \(\d+\)\.csv$", fn):
        continue
    m = re.search(r" - (.+?)\.csv$", fn)
    if not m:
        continue
    name = m.group(1)
    if name == FLOW:
        continue
    clean = re.sub(r"\uff08[^\uff09]*\uff09$", "", name).strip()
    d = extract(p)
    if len(d) < 2:
        print("  SKIP(中身なし):", clean)
        continue
    defs[clean] = d

print("sheets: %d" % len(defs))
for k in sorted(defs):
    print("  %-20s rows=%-4d" % (k, len(defs[k])))

OUT = r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts"
f = io.open(OUT, "w", encoding="utf-8")
f.write("// [HEARING_SHEET_DEFS_V5 2026-10-29] 自動生成 (_rebuild_v5.py)\n")
f.write("// 雛形の『行構成も列位置も』そのまま保持する。\n")
f.write("//   社内用の列は値を空にするだけ（列も行も削らない＝行番号が雛形と一致）\n")
f.write("//   回答欄(TRUE/FALSE)は □\n")
f.write("// ⚠ 手で編集しないこと。雛形が変わったら _rebuild_v5.py を再実行する。\n")
f.write("export const HEARING_SHEET_DEFS: Record<string, string[][]> = ")
f.write(json.dumps(defs, ensure_ascii=False, indent=1))
f.write("\n")
f.close()
print("\nwrote", OUT)
