# -*- coding: utf-8 -*-
# 睡眠姦S・人身売買Sシリーズのグループ定義・push・outfits_refを調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
for m in re.finditer(r"\{key:'([^']+)',label:\"([^\"]*(?:睡眠姦|人身売買)[^\"]*)\",fn:id => /\^(char_[a-z0-9_]+_)/", s):
    print('GD:', m.group(1), '|', m.group(2), '|', m.group(3))
print('---pushes---')
for pref in ['suimin', 'jinshin']:
    rows = re.findall(r"push\(\{id:'(char_" + pref + r"_s\d+_[a-z0-9_]*)'[^\n]*?outfits_ref:\"(S\d+)\"", s)
    seen = {}
    for a, b in rows:
        seen.setdefault(b, []).append(a)
    print(pref, 'with ref:', len(rows))
    for b in sorted(seen):
        print(' ', b, len(seen[b]), seen[b][0])
    all_push = re.findall(r"push\(\{id:'(char_" + pref + r"_s\d+_[a-z0-9_]*)'", s)
    print(pref, 'total push:', len(all_push))
