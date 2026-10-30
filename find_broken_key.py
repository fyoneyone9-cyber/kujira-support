# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
# L24686の行でcolumn 1361付近を確認
l = lines[24685]
print(f'Length: {len(l)}')
print(f'Around col1361: {repr(l[1350:1400])}')
# 壊れたkey:labelパターンを探す
import re
for i, line in enumerate(lines):
    if re.search(r"'\s*:\s*label:", line) or re.search(r'":\s*label:', line) or re.search(r"['\"]:['\"]", line):
        if 'rape_legal' in line or 'key:label' in line.replace(' ',''):
            print(f'L{i+1}: {line.rstrip()[:150]}')
