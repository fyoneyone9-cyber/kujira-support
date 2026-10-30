# -*- coding: utf-8 -*-
# 魔法少女・触手系グループの定義とIDパターン・体数を調査
import re, sys, io, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
kw = ['魔法少女', '触手', '魔法園児']
seen = set()
for m in re.finditer(r"key:\s*'([^']+)',\s*label:\s*[\"']([^\"']*(?:魔法少女|触手|魔法園児)[^\"']*)[\"']", s):
    k = (m.group(1), m.group(2))
    if k in seen:
        continue
    seen.add(k)
    print('GD:', m.group(1), '|', m.group(2))
print('=== id counts ===')
for pat in ['char_mahou_shoujo_', 'char_manga_mahou_', 'char_tentacle_', 'char_tent_', 'char_mahou_youchien_', 'char_mahou_']:
    ids = set(re.findall(r"id:\s*['\"](" + pat + r"[a-zA-Z0-9_]+)['\"]", s))
    print(pat, len(ids))
