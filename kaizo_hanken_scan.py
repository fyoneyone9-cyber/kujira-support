# -*- coding: utf-8 -*-
# 改造版権キャラ10グループのGD定義とID実体を調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
kw = ['改造AKB', '改造FF', '改造アニメ', '改造エヴァ', '改造セーラー', '改造ダイ', '改造鬼滅', '改造芸能人', '改造レイ', '改造エマ', '改造版権']
seen = set()
for m in re.finditer(r"key:\s*'([^']+)',\s*label:\s*[\"']([^\"']+)[\"'][^\n]{0,220}", s):
    if any(t in m.group(2) for t in kw):
        k = m.group(0)[:240]
        if k in seen: continue
        seen.add(k)
        print('GD:', k.replace('\n','\\n'))
        print('---')
