# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# cap1.35 の定義箇所・QRのkeep/protect系を探す
for i, l in enumerate(lines):
    if 'cap1.35' in l or 'cap_max' in l or '_qr_protect' in l or 'outfit_tag' in l or 'OUTFIT_TAG' in l or ('cap' in l and '1.35' in l and 'def ' not in l):
        print(f'L{i+1}: {l.rstrip()[:120]}')
