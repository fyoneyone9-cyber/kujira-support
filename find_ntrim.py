# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\quality_rules.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'ntrim' in l or 'nkeep' in l or 'trim' in l.lower() and 'def' not in l:
        print(f'L{i+1}: {l.rstrip()[:140]}')
