# -*- coding: utf-8 -*-
# ロリコン天国シリーズのグループ定義・push・outfits_refを調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
for m in re.finditer(r"\{key:'([^']+)',label:\"([^\"]*天国[^\"]*)\",fn:id => /\^(char_[a-z0-9_]+_)/", s):
    print('GD:', m.group(1), '|', m.group(2), '|', m.group(3))
# match形式も
for m in re.finditer(r"key:\s*'([^']+)',\s*label:\s*'([^']*天国[^']*)'", s):
    print('GD2:', m.group(1), '|', m.group(2))
