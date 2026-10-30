# -*- coding: utf-8 -*-
"""コードが期待するシート名と、雛形の実タブ名を突き合わせる。"""
import io, json

t = io.open(r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts", encoding="utf-8").read()
defs = json.loads(t[t.index("= ") + 2:].strip())

g = io.open(r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js", encoding="utf-8").read()
i = g.index("var EQUIP_SHEETS")
j = g.index("function showDialog")
block = g[i:j]

import re
code_names = set(re.findall(r"'([^']+)'", block))
# キー名(pms等)を除く
code_names = {n for n in code_names if not re.match(r"^[a-z0-9_]+$", n)}

print("=== コードが残そうとするシート名 ===")
for n in sorted(code_names):
    mark = "OK " if n in defs else "❌ 雛形に無い"
    print("  %-22s %s" % (n, mark))

print("\n=== 雛形(CSV由来)にあるシート名 ===")
for n in sorted(defs):
    mark = "" if n in code_names else "  ← コードが知らない＝常に削除対象"
    print("  %-22s%s" % (n, mark))
