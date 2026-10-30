# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'CLOTHING_DISAPPEAR' in l or ('leash' in l and ('neg' in l.lower() or 'drop' in l.lower() or 'remove' in l.lower() or 'strip' in l.lower())):
        print(f'L{i+1}: {l.rstrip()[:140]}')
