# -*- coding: utf-8 -*-
# ラベル生出現位置の前後コンテキストを直接表示してID形式を目視特定
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
for t in ['捕食ミア', 'エンタコール', '無乳 幼女', '囚われルシア']:
    for m in list(re.finditer(re.escape(t), s))[:2]:
        i = m.start()
        print('===', t, 'at', i)
        print(repr(s[max(0,i-350):i+100])[-500:])
        print('---')
