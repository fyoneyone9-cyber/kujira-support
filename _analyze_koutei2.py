# -*- coding: utf-8 -*-
"""工程管理表の判定精度を検証する。
区分だけでなく、作業名・詳細からも要否を判断できないか調べる。
"""
import io, json, re, collections

t = io.open(r"C:\GensparkClaw\kujira-support\src\lib\kouteiDef.ts", encoding="utf-8").read()
rows = json.loads(t[t.index("KOUTEI_ROWS: string[][] = ") + len("KOUTEI_ROWS: string[][] = "):
                    t.index("\n\n// \u533a\u5206")].strip())

print("総行数: %d" % len(rows))
print("\n=== 区分ごとの作業内容 ===")
by = collections.OrderedDict()
for r in rows[3:]:
    if len(r) < 4:
        continue
    cat = (r[2] or "").strip()
    task = (r[3] or "").strip()
    if not cat:
        continue
    by.setdefault(cat, []).append(task)

for cat, tasks in by.items():
    print("\n[%s] %d行" % (cat, len(tasks)))
    for x in tasks:
        print("    %s" % x[:40])
