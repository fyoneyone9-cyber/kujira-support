# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i in range(24680, min(24695, len(lines))):
    print(f'L{i+1}: {repr(lines[i].rstrip()[:150])}')
