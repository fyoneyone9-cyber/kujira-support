# -*- coding: utf-8 -*-
# char_tousatsu_ の出現箇所を全部確認
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
idxs = [m.start() for m in re.finditer(r'char_tousatsu_', s)]
print('occurrences:', len(idxs))
ids = set(re.findall(r"id:\s*'(char_tousatsu_[a-z0-9_]+)'", s))
print('ids:', sorted(ids))
for i in idxs[:5]:
    print(repr(s[max(0,i-80):i+120]))
    print('---')
