# -*- coding: utf-8 -*-
"""ヘッダの時計（17:41 / 2026年 10月）を描画している箇所を探す。"""
import io, re, os

base = r"C:\GensparkClaw\kujira-support\src"
pat = re.compile(r"getHours|getMinutes|toLocaleTimeString|getFullYear|getMonth|\u5e74|\u6708")
for root, dirs, files in os.walk(base):
    for fn in files:
        if not fn.endswith((".tsx", ".ts")):
            continue
        p = os.path.join(root, fn)
        L = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
        for i, l in enumerate(L, 1):
            if re.search(r"getHours|getMinutes|toLocaleTimeString", l) or \
               (re.search(r"getFullYear|getMonth", l) and "<" in l) or \
               re.search(r"\{\s*\w+\s*\}\s*\u5e74", l):
                print("%s:%d| %s" % (os.path.relpath(p, base), i, l.strip()[:130]))
