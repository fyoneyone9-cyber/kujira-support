# -*- coding: utf-8 -*-
# 非push出現箇所の周辺を詳細表示（巨大1行対策で前後200文字のみ）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\AI\ComfyUI\dashboard.html'
s = open(p, encoding='utf-8').read()
for m in re.finditer(r'char_miko_s', s):
    i = m.start()
    ctx = s[max(0,i-150):i+100]
    if 'CHAR_TEMPLATES.female.push' in ctx:
        continue
    print('POS', i)
    print(repr(ctx))
    print('---')
