# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'insertion' in l and ('detect' in l or '=' in l or 'False' in l or 'True' in l or 'flag' in l.lower()):
        if 'dbg_sex' in l or 'insertion=' in l or '_insertion' in l or 'is_insertion' in l:
            print(f'L{i+1}: {l.rstrip()[:150]}')
