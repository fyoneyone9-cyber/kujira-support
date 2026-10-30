# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\quality_rules.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
start = None
for i, l in enumerate(lines):
    if 'def _rule_composition' in l:
        start = i; break
if start:
    for l in lines[start:start+50]:
        print(l.rstrip()[:140])
