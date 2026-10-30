# -*- coding: utf-8 -*-
# 削除前調査: char_miko_s 関連の登録箇所(registerGenre/GROUP_DEFS/CATEGORIES等)を洗い出す
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\AI\ComfyUI\dashboard.html'
s = open(p, encoding='utf-8').read()
pat = 'char_miko_s'
idxs = [m.start() for m in re.finditer(re.escape(pat), s)]
print('total occurrences:', len(idxs))
# push行以外の出現箇所（registerGenre等）を表示
lines_seen = set()
for i in idxs:
    ls = s.rfind('\n', 0, i) + 1
    le = s.find('\n', i)
    line = s[ls:le]
    if 'CHAR_TEMPLATES.female.push' in line:
        continue
    key = line[:120]
    if key in lines_seen:
        continue
    lines_seen.add(key)
    print('POS', i, ':', line[:300])
# registerGenre miko
for m in re.finditer(r"registerGenre\(\{[^}]*miko[^}]*\}\)", s):
    print('REG:', m.group(0)[:300])
