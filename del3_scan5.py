# -*- coding: utf-8 -*-
# char_tousatsu_ 全25出現の分類（定義実体の形式を特定する）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
for m in re.finditer(r'char_tousatsu_[a-zA-Z0-9_]*', s):
    tok = m.group(0)
    i = m.start()
    ctx = s[max(0,i-60):i+80].replace('\n', '\\n')
    print(tok, '||', ctx[:160])
    print('---')
