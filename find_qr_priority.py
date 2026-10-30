# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# quality_rules.py の apply_quality_rules / priority_tags の扱いを確認
for i, l in enumerate(lines):
    if 'priority_tags' in l or 'prio_set' in l or 'above_cap' in l or 'two-tier' in l:
        print(f'L{i+1}: {l.rstrip()[:130]}')
