# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    lines = f.readlines()

l = lines[432259]
print('line:', l[:500])
# outfits内容
idx = l.find('outfits:')
print('\noutfits portion:', l[idx:idx+500])
