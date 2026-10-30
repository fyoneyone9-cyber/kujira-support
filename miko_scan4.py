# -*- coding: utf-8 -*-
import re, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\AI\ComfyUI\dashboard.html'
s = open(p, encoding='utf-8').read()

# 1) 全miko s系キャラのoutfits_refをマップ
rows = re.findall(r"id:'(char_miko_s\d+_[a-z_]+)'[^\n]*?outfits_ref:\"(S\d+)\"", s)
print(len(rows))
for a,b in rows: print(a,b)

# 2) outfits_refの仕組み: S0572定義を探す
for key in ['S0571','S0572']:
    i = s.find('"'+key+'"')
    print('---', key, 'occurrences:', s.count('"'+key+'"'))
# OUTFITS_REF DB 定義箇所を探す
m = re.search(r"(OUTFIT[S]?_(?:REF|DB|STORE)[A-Z_]*)\s*=", s)
print('db name:', m.group(1) if m else None)
idx = s.find('outfits_ref')
print(repr(s[idx-200:idx+100]))
