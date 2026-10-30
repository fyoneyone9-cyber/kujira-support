# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\pose_presets.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Total: {len(lines)} lines')
# doggy と removed の箇所
for i, l in enumerate(lines):
    if 'doggy' in l or 'remove' in l.lower() or 'leash' in l or 'collar' in l or 'on all fours' in l:
        print(f'L{i+1}: {l.rstrip()[:140]}')
