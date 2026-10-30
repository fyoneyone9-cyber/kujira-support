# -*- coding: utf-8 -*-
# manga_mahou キャラ定義の実体と、tentacle配列ブロックの範囲を特定
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()

# 1) manga_mahou キャラ定義（id: 'xxx' スペースあり形式）
ids = sorted(set(re.findall(r"id:\s*['\"](char_manga_mahou_[a-zA-Z0-9_]+)['\"]", s)))
print('manga_mahou ids:', len(ids), ids[:25])

# 2) manga_mahou の生出現で id らしきもの
toks = sorted(set(re.findall(r"char_manga_mahou_[a-zA-Z0-9_]+", s)))
print('tokens:', toks[:30])

# 3) tentacle 配列ブロック: どの変数か（youjo_A の前方を遡る）
i = s.find("id: 'char_tentacle_youjo_A'")
back = s[max(0,i-6000):i]
for kwd in ['push(', '= [', 'concat', 'TEMPLATES']:
    print(kwd, back.rfind(kwd))
print(repr(back[-600:]))
