# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\outfit_sets.json','r',encoding='utf-8') as f:
    d = json.load(f)
print('Keys:', list(d.keys())[:30])
print()
if 'S0252' in d:
    outfits = d['S0252']
    print(f'S0252 has {len(outfits)} outfits:')
    for i, o in enumerate(outfits):
        print(f'  {i+1:02d}: {o.get("label","?")}')
        print(f'       {o.get("prompt","")[:80]}')
