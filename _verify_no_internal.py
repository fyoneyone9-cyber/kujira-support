# -*- coding: utf-8 -*-
"""生成した hearingSheetDefs.ts に社内用の情報が残っていないか検査する。
お客様送付用なので、ここが漏れると社内情報が外部に出る。"""
import io, json, re, sys

p = r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts"
t = io.open(p, encoding="utf-8").read()
j = t[t.index("= ") + 2:].strip()
defs = json.loads(j)

NG = [
    "\u30d2\u30a2\u30ea\u30f3\u30b0\u30b7\u30fc\u30c8\u3078",       # 〜のヒアリングシートへ
    "DMS\u5165\u529b\u9805\u76ee",                                  # DMS入力項目
    "\u30bf\u30d6\u30ec\u30c3\u30c8\u306e\u5834\u5408\u4e0d\u8981",  # タブレットの場合不要
    "\u793e\u5185\u7528",                                            # 社内用
    "\u7530\u4e2d\u793e\u9577",                                      # 田中社長
    "\u55b6\u696d\u306b\u78ba\u8a8d",                                # 営業に確認
    "\u30af\u30e9\u30a4\u30a2\u30f3\u30c8ID",                        # クライアントID
    "\u975e\u8868\u793a\u306b\u3057\u3066\u304f\u3060\u3055\u3044",  # 非表示にしてください
]

print("sheets: %d" % len(defs))
bad = 0
for name, rows in defs.items():
    flat = " ".join(" ".join(r) for r in rows)
    hits = [n for n in NG if n in flat]
    if hits:
        bad += 1
        print("  \U0001f534 %s : %s" % (name, hits))
        for r in rows:
            line = " | ".join(r)
            if any(n in line for n in NG):
                print("        %s" % line[:150])
    else:
        print("  OK %-18s rows=%d" % (name, len(rows)))

print("\n%s" % ("PASS - 社内用情報の残留なし" if bad == 0 else "FAIL - %d シートに残留" % bad))
sys.exit(1 if bad else 0)
