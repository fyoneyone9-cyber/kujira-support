# -*- coding: utf-8 -*-
# 改造ジブリール/ティファv2/2Bv2/ミクv2/歌手v2/テイラーv2 のGD定義とID実体を調査（世界DUOは対象外）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
kw = ['改造ジブリール', '改造ティファ', '改造2B', '改造ミク', '改造歌手', '改造テイラー', '世界DUO']
seen = set()
for m in re.finditer(r"key:\s*'([^']+)',\s*label:\s*[\"']([^\"']+)[\"'][^\n]{0,200}", s):
    if any(t in m.group(2) for t in kw):
        k = m.group(0)[:220]
        if k in seen: continue
        seen.add(k)
        print('GD:', k.replace('\n','\\n'))
        print('---')
