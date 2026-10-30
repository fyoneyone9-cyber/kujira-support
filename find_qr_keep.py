# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'slave_collar' in l or 'collar with leash' in l or 'being led by leash' in l or ('collar' in l and 'keep' in l):
        print(f'L{i+1}: {l.rstrip()[:120]}')
