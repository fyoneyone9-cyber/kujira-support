# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\outfit_sets.json','r',encoding='utf-8') as f:
    d = json.load(f)

# S0252の内容
print('S0252 full:')
print(json.dumps(d['S0252'], ensure_ascii=False, indent=2)[:500])

# S5系で使われているoutfits_refキーを探す（dashboard.htmlで）
with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    c = f.read()
import re
refs = re.findall(r"outfits_ref:['\"]([^'\"]+)['\"]", c)
from collections import Counter
cnt = Counter(refs)
print('\nTop outfit refs:')
for k, v in cnt.most_common(15):
    in_json = k in d
    print(f'  {k}: {v}x, in_json={in_json}')
