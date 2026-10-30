# -*- coding: utf-8 -*-
# 調査: 巫女系キャラIDと構造を把握する
import re
p = r'C:\AI\ComfyUI\dashboard.html'
s = open(p, encoding='utf-8', errors='strict').read()
ids = re.findall(r"id:\s*'([^']*miko[^']*)'", s)
print("miko id count:", len(ids))
for i in ids[:80]:
    print(i)
# ラベルに「巫女」を含むキャラも
labels = re.findall(r"id:\s*'([^']+)',\s*label:\s*'([^']*巫女[^']*)'", s)
print("label巫女 count:", len(labels))
for a, b in labels[:80]:
    print(a, "|", b)
