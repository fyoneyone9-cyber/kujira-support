# -*- coding: utf-8 -*-
# cats[]等で 'miko_s1' (char_なし) を参照している箇所を確認
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\AI\ComfyUI\dashboard.html'
s = open(p, encoding='utf-8').read()
for m in re.finditer(r"'miko_s\d+'", s):
    i = m.start()
    ctx = s[max(0,i-120):i+60]
    if 'char_miko' in ctx:
        continue
    print('POS', i, repr(ctx))
    print('---')
print('done')
