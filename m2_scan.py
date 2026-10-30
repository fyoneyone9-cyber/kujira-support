# -*- coding: utf-8 -*-
# ロリ人形・愛玩児飼育シリーズのID・outfits_ref・グループ定義を調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
# ラベルに「ロリ人形」「愛玩児」を含むグループ定義
for m in re.finditer(r"\{key:'([^']+)',label:\"([^\"]*(?:ロリ人形|愛玩児)[^\"]*)\",fn:id => /\^(char_[a-z0-9_]+_)/", s):
    print('GD:', m.group(1), '|', m.group(2), '|', m.group(3))
print('---pushes---')
rows = re.findall(r"push\(\{id:'(char_(?:loli_?doll|aigan)[a-z0-9_]*)'[^\n]*?outfits_ref:\"(S\d+)\"", s)
print(len(rows))
seen = {}
for a, b in rows:
    seen.setdefault(b, []).append(a)
for b in sorted(seen):
    print(b, len(seen[b]), seen[b][0])
