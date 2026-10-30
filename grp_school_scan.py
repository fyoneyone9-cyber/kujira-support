# -*- coding: utf-8 -*-
# 対象グループ（小学生/幼女系/まんこ図鑑/保健体育系/触手保健/カルト教団S）のGD定義とIDパターンを調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
kw = ['小学生', '幼女', '幼児', 'まんこ図鑑', '保健体育', '触手保健', 'カルト教団']
seen = set()
for m in re.finditer(r"key:\s*'([^']+)',\s*label:\s*[\"']([^\"']+)[\"']", s):
    if any(t in m.group(2) for t in kw):
        k = (m.group(1), m.group(2))
        if k in seen: continue
        seen.add(k)
        print('GD:', m.group(1), '|', m.group(2))
