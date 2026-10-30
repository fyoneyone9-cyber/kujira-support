# -*- coding: utf-8 -*-
# 近親Sシリーズのグループ定義・push・outfits_refを調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
for m in re.finditer(r"\{key:'([^']+)',label:\"([^\"]*近親[^\"]*)\",fn:id => /\^(char_[a-z0-9_]+_)/", s):
    print('GD:', m.group(1), '|', m.group(2), '|', m.group(3))
print('---pushes---')
rows = re.findall(r"push\(\{id:'(char_kinshin[a-z0-9_]*)'[^\n]*?outfits_ref:\"(S\d+)\"", s)
print(len(rows))
seen = {}
for a, b in rows:
    seen.setdefault(b, []).append(a)
for b in sorted(seen):
    print(b, len(seen[b]), seen[b][0])
# outfits_refなしpushも確認
all_push = re.findall(r"push\(\{id:'(char_kinshin[a-z0-9_]*)'", s)
print('total kinshin push:', len(all_push))
