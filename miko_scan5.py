# -*- coding: utf-8 -*-
# S0572〜S0581の全ラベルと件数を確認（S間でどの程度同じか）
import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
d = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json', encoding='utf-8'))
for n in range(572, 582):
    k = 'S0%d' % n
    items = d[k]['items']
    print('='*20, k, len(items))
    for it in items[:30]:
        print(' ', it['label'])
