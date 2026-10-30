# -*- coding: utf-8 -*-
# 温泉盗撮・深夜尾行・透明人間のGD定義とID実体を調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
seen = set()
for m in re.finditer(r"key:\s*'([^']+)',\s*label:\s*[\"']([^\"']*(?:温泉盗撮|深夜尾行|透明人間|盗撮・尾行)[^\"']*)[\"'][^\n]{0,200}", s):
    k = m.group(0)[:220]
    if k in seen: continue
    seen.add(k)
    print('GD:', k.replace('\n','\\n'))
    print('---')
print('=== ids ===')
for p in ['char_onsen_', 'char_biko_', 'char_shinya_', 'char_toumei_', 'char_invisible_']:
    ids = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](" + p + r"[a-zA-Z0-9_]*)[\"']", s)))
    print(p, len(ids), ids[:10])
