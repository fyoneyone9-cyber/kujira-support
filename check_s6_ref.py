# -*- coding: utf-8 -*-
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    c = f.read()

# S6/S7のoutfits_refを確認
for pat in ['nichijou6', 'nichijou7', 'nichijou5']:
    m = re.search(r"id:['\"]char_kaizo_" + pat + r"_jk_A['\"][^}]*outfits_ref:['\"]([^'\"]+)['\"]", c)
    if m:
        ref = m.group(1)
        print(f'{pat} jk_A outfits_ref: {ref}')
        # JSON内のシーン確認
        d = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json','r',encoding='utf-8'))
        if ref in d:
            print(f'  -> {len(d[ref])} outfits:')
            for o in d[ref]:
                print(f'    - {o.get("label","?")}')
