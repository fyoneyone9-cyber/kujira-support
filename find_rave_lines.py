# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'char_rape_legal_' in l and ("id:'" in l or 'id:"' in l):
        print(f'L{i+1}: {l.rstrip()[:120]}')
        # 前後3行も表示
        for j in range(max(0,i-1), min(len(lines),i+4)):
            print(f'  [{j+1}] {lines[j].rstrip()[:100]}')
        print()
