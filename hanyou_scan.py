# -*- coding: utf-8 -*-
# 汎用キャラ（男性／職業・役割）のGD定義とIDパターンを調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
seen = set()
for m in re.finditer(r"key:\s*'([^']+)',\s*label:\s*[\"']([^\"']*(?:男性|職業・役割|汎用)[^\"']*)[\"'][^\n]{0,250}", s):
    k = m.group(0)[:260]
    if k in seen: continue
    seen.add(k)
    print('GD:', k.replace('\n', '\\n'))
    print('---')
