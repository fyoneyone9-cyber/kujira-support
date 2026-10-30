# -*- coding: utf-8 -*-
"""[GAS_PAIR_AUDIT_V1 2026-10-29] コード.gs と dialog の整合性を検査する。

貼り替え後に動かない事故が続いているので、
「ダイアログが呼ぶ関数」と「コード側の定義」が一致しているか機械的に確認する。
"""
import io, re

G = io.open(r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js", encoding="utf-8").read()
D = io.open(r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html", encoding="utf-8").read()

called = sorted(set(re.findall(r"\.(\w+)\(\s*(?:LAST_EQUIPS|\{|\)|$)", D)) |
                set(re.findall(r"\}\)\.(\w+)\(", D)))
defined = set(re.findall(r"function\s+(\w+)\s*\(", G))

print("=== ダイアログが呼ぶ関数 ===")
ng = []
for f in called:
    if f in ("then", "catch", "forEach", "map", "filter", "find", "join", "push",
             "replace", "split", "trim", "indexOf", "test", "slice", "getElementById",
             "querySelector", "setValue", "getValue", "writeText", "parse", "stringify"):
        continue
    ok = f in defined
    if not ok:
        ng.append(f)
    print("  %-18s %s" % (f, "OK" if ok else "NG コード側に無い"))

print("\n=== コード側の主要関数 ===")
for f in ["onOpen", "showDialog", "getVersion", "getSheetNames", "suggestSheets",
          "createCopy", "fillInfo"]:
    print("  %-18s %s" % (f, "OK" if f in defined else "NG 未定義"))

print("\n=== createCopy が受け取るキー ===")
i = G.index("function createCopy")
seg = G[i:i + 1200]
for k in ["p.sheets", "p.client", "p.property", "p.address", "p.contact",
          "p.tel", "p.email", "p.rooms"]:
    print("  %-14s %s" % (k, "使用" if k in G else "-"))

print("\n整合性:", "OK" if not ng else "NG " + str(ng))
