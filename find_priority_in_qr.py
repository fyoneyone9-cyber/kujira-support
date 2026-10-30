# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\quality_rules.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Total lines: {len(lines)}')
for i, l in enumerate(lines):
    if 'priority_tags' in l or 'prio_set' in l or 'above_cap' in l or 'cap_exempt' in l:
        print(f'L{i+1}: {l.rstrip()[:140]}')
