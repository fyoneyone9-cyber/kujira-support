# -*- coding: utf-8 -*-
# 教師と教え子S・コスプレ図鑑のグループ定義・push・outfits_refを調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
for m in re.finditer(r"key:\s*'([^']+)',\s*label:\s*[\"']([^\"']*(?:教師と教え子|コスプレ図鑑)[^\"']*)[\"']", s):
    print('GD:', m.group(1), '|', m.group(2))
print('---pushes---')
for pref in ['kyoushi', 'cosplay']:
    rows = re.findall(r"push\(\{id:'(char_" + pref + r"[a-z0-9_]*)'[^\n]*?outfits_ref:\"(S\d+)\"", s)
    seen = {}
    for a, b in rows:
        seen.setdefault(b, []).append(a)
    print('===', pref, 'with ref:', len(rows))
    for b in sorted(seen):
        print(' ', b, len(seen[b]), seen[b][0])
    allp = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](char_" + pref + r"[a-zA-Z0-9_]*)[\"']", s)))
    print(pref, 'total ids:', len(allp), allp[:8])
