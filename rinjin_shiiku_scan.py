# -*- coding: utf-8 -*-
# 隣人管理人S・ロリ飼育施設S のグループ定義・push・outfits_refを調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
for m in re.finditer(r"key:\s*'([^']+)',\s*label:\s*[\"']([^\"']*(?:隣人管理人|飼育施設)[^\"']*)[\"']", s):
    print('GD:', m.group(1), '|', m.group(2))
print('===patterns===')
for m in re.finditer(r"\{key:'([^']+)',label:\"([^\"]*(?:隣人管理人|飼育施設)[^\"]*)\",fn:id => /\^(char_[a-z0-9_]+_)/", s):
    print('FN:', m.group(1), '|', m.group(2), '|', m.group(3))
