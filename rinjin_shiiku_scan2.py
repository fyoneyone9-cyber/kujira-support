# -*- coding: utf-8 -*-
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
for pref in ['rinjin', 'breedfac']:
    rows = re.findall(r"push\(\{id:'(char_" + pref + r"_s\d+_[a-z0-9_]*)'[^\n]*?outfits_ref:\"(S\d+)\"", s)
    seen = {}
    for a, b in rows:
        seen.setdefault(b, []).append(a)
    print('===', pref, 'with ref:', len(rows))
    for b in sorted(seen):
        print(' ', b, len(seen[b]), seen[b][0])
    all_push = re.findall(r"push\(\{id:'(char_" + pref + r"_s\d+_[a-z0-9_]*)'", s)
    print(pref, 'total push:', len(all_push))
