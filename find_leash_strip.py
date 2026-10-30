# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
# leash / collar with leash を除去・置換する処理
for i, l in enumerate(lines):
    if ('leash' in l or 'collar' in l) and ('replace' in l or 'remove' in l or 'strip' in l or 're.sub' in l or 'pop' in l or 'drop' in l):
        print(f'L{i+1}: {l.rstrip()[:140]}')
