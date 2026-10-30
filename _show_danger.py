# -*- coding: utf-8 -*-
import io, re
base = r"C:\GensparkClaw\kujira-support"
page = io.open(base + r"\src\app\(app)\delivery\page.tsx", encoding="utf-8").read().split("\n")
imp = io.open(base + r"\src\app\api\delivery\import-csv\route.ts", encoding="utf-8").read().split("\n")

print("=== page.tsx : status / delivery_due_date を書く箇所 ===")
for i, l in enumerate(page, 1):
    if re.search(r"patch\(|JSON\.stringify\(\{\s*id", l) and re.search(r"status|delivery_due_date", l):
        print("%5d| %s" % (i, l.strip()[:170]))

print("\n=== import-csv : status / delivery_due_date の決定箇所 ===")
for i, l in enumerate(imp, 1):
    if re.search(r"\bstatus\b|delivery_due_date", l):
        print("%5d| %s" % (i, l.strip()[:170]))
