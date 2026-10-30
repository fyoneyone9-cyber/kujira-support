# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    c = f.read()

# outfits_refを解決するコードを探す
for kw in ['outfits_ref', 'resolveOutfits', 'getOutfits', 'outfit_ref']:
    hits = [m.start() for m in re.finditer(kw, c)]
    if hits:
        print(f'{kw}: {len(hits)} hits, first at {hits[0]}')
        print(c[hits[0]:hits[0]+300])
        print('---')
        break
