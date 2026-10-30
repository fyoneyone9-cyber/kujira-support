# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    c = f.read()
for m in re.finditer(r'char_rape_legal_', c):
    ctx = c[m.start()-20:m.start()+80]
    print(ctx[:100])
    print()
