# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    lines = f.readlines()

l = lines[432259]
print('line length:', len(l))
print('has outfits:', 'outfits' in l)
print('first 300:', l[:300])

# outfits_ref があるかも
m2 = re.search(r"outfits_ref:'([^']+)'", l)
if m2:
    print('outfits_ref:', m2.group(1))
