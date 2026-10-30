# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
# L22250-22270
for i in range(22248, min(22272, len(lines))):
    print(f'L{i+1}: {lines[i].rstrip()[:120]}')
