# -*- coding: utf-8 -*-
"""ヒアリングシート欄の開閉ロジックを確認する。"""
import io, re

p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
L = io.open(p, encoding="utf-8").read().split("\n")
for i, l in enumerate(L, 1):
    if re.search(r"toggleSection|openSections|hearing_|expanded", l):
        print("%5d| %s" % (i, l.strip()[:160]))
