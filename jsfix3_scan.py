# -*- coding: utf-8 -*-
# block25 (html line 411711) + js line 3652 の孤立トークン周辺を確認
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
lines = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read().split('\n')
center = 411711 + 3652 - 1
for i in range(center-8, center+6):
    print(i+1, repr(lines[i])[:160])
