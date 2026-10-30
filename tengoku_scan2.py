# -*- coding: utf-8 -*-
# ロリコン天国S 全定義形式・push・outfits_refを調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
# GD定義の周辺を確認
i = s.find("'lolicon_heaven_s1'")
print(repr(s[max(0,i-100):i+300]))
print('===')
# char idパターンを拾う
ids = set(re.findall(r"(char_lolicon_heaven_s\d+_[a-zA-Z0-9_]+)", s))
print('ids found:', len(ids))
# 他のidパターン候補
for pat in ['char_loliheaven', 'char_lolicon']:
    cnt = s.count(pat)
    print(pat, cnt)
