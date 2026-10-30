# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    lines = f.readlines()

# S5 jk_Aのブロック行番号を特定
start = None
for i, l in enumerate(lines):
    if "char_kaizo_nichijou5_jk_A" in l and "id:" in l:
        start = i
        break
print(f'S5 jk_A starts at L{start+1}')
if start:
    # });まで読む
    for j in range(start, min(start+200, len(lines))):
        print(f'L{j+1}: {lines[j].rstrip()[:100]}')
        if lines[j].rstrip().endswith(');') and j > start:
            break
