# -*- coding: utf-8 -*-
# ロリ風俗Sシリーズのグループ定義・push・outfits_refを調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
for m in re.finditer(r"\{key:'([^']+)',label:\"([^\"]*風俗[^\"]*)\",fn:id => /\^(char_[a-z0-9_]+_)/", s):
    print('GD:', m.group(1), '|', m.group(2), '|', m.group(3))
