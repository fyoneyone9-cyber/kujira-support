# -*- coding: utf-8 -*-
# 手懐けシリーズのグループ定義・push・outfits_refを調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
for m in re.finditer(r"\{\s*key:\s*'([^']+)',\s*label:\s*[\"']([^\"']*手懐け[^\"']*)[\"'],\s*(?:fn|match):", s):
    print('GD:', m.group(1), '|', m.group(2))
# fn内のidパターンも拾う
for m in re.finditer(r"key:'([^']+)',label:\"([^\"]*手懐け[^\"]*)\",fn:id => /\^(char_[a-z0-9_]+_)/", s):
    print('GD2:', m.group(1), '|', m.group(2), '|', m.group(3))
