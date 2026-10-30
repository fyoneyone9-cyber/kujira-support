# -*- coding: utf-8 -*-
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    c = f.read()
d = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json','r',encoding='utf-8'))

# 狂気改造系でシーンが入ってるキャラを探す
kaizo = re.findall(r"id:['\"]char_kaizo_nichijou[^'\"]*['\"].*?outfits_ref:['\"]([^'\"]+)['\"]", c)
for ref in set(kaizo):
    if ref in d and len(d[ref]) > 1:
        print(f'ref={ref}, count={len(d[ref])}')
        for o in d[ref][:3]:
            print(f'  {o.get("label","?")}')

# gen_nichijou2を確認
if 'gen_nichijou2' in d:
    print(f'\ngen_nichijou2: {len(d["gen_nichijou2"])} outfits')
    for o in d['gen_nichijou2']:
        print(f'  {o.get("label","?")} | {str(o.get("prompt",""))[:60]}')
