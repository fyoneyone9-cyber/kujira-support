# -*- coding: utf-8 -*-
# POV系9グループのグループ定義・push・outfits_refを調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
# GD（fn形式・match形式・registerGenre形式）でPOVを含むラベル
for m in re.finditer(r"key:\s*'([^']+)',\s*label:\s*[\"']([^\"']*POV[^\"']*)[\"']", s):
    print('GD:', m.group(1), '|', m.group(2))
print('===')
# idパターン候補
import collections
ids = re.findall(r"push\(\{\s*\n*\s*id:\s*['\"](char_[a-z0-9_]*pov[a-z0-9_]*)['\"]", s, re.IGNORECASE)
cnt = collections.Counter(re.sub(r'_(s\d+_)?[a-z]+_?[a-z]*$', '', x) for x in ids)
print('pov push ids:', len(ids))
pref = collections.Counter()
for x in ids:
    m2 = re.match(r'(char_[a-z0-9]+_pov|char_pov[a-z0-9_]*?)_', x)
    pref[m2.group(1) if m2 else x] += 1
for k, v in sorted(pref.items()):
    print(' ', k, v)
