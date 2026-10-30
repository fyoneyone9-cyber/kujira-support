# -*- coding: utf-8 -*-
# 残存7箇所の内容確認
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
for i in [745527, 937728, 937851, 937977, 990942, 992679, 1014560]:
    print('POS', i)
    print(repr(s[max(0,i-150):i+150]))
    print('---')
