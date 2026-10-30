# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
# quality_rules.py の _load 関数を確認
with open(r'C:\AI\ComfyUI\quality_rules.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'def _load' in l or '_RULES_DIR' in l or 'pos_drop' in l:
        print(f'L{i+1}: {l.rstrip()[:140]}')
