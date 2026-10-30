# -*- coding: utf-8 -*-
# 工場シリーズ char_factory_* の全ID・GD定義・push構造（壊れたblock25含む）を調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
ids = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](char_factory_[a-zA-Z0-9_]+)[\"']", s)))
print('factory ids:', len(ids))
for x in ids:
    print('  ', x)
# GD定義
for m in re.finditer(r"key:\s*'([^']+)',\s*label:\s*[\"']([^\"']*)[\"'][^\n]{0,80}char_factory[^\n]{0,80}", s):
    print('GD:', m.group(0)[:200])
    print('---')
# refs
refs = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"']char_factory_[a-zA-Z0-9_]+[\"'][^\n]*?outfits_ref:[\"'](S\d+)[\"']", s)))
print('refs(inline):', refs)
refs2 = sorted(set(re.findall(r"char_factory_[^\n]{0,400}?outfits_ref:[\"'](S\d+)[\"']", s, re.DOTALL)))
print('refs(multi):', refs2)
# 壊れた '  );' 行の位置再確認
lines = s.split('\n')
for i, l in enumerate(lines):
    if l.strip() == ');' and 410000 < i < 420000:
        print('orphan ); at line', i+1)
