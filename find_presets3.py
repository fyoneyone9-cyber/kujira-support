# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    c = f.read()
# AOM3 / majic を含む行を全部出力
for i, line in enumerate(c.split('\n')):
    if 'AOM3' in line or 'majic' in line or '\u30a2\u30cb\u30e1' in line:
        if 'option' in line or 'STYLE' in line or 'preset' in line.lower():
            print(f'L{i+1}: {line.strip()[:200]}')
