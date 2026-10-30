# -*- coding: utf-8 -*-
# 「ロリ (2体)」グループ（ティファ/エアリス 各24シーン）のGD定義とID実体を調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
# GD: label に「ロリ」単体のグループ
seen = set()
for m in re.finditer(r"key:\s*'([^']+)',\s*label:\s*[\"']([^\"']*ロリ[^\"']*)[\"'][^\n]{0,180}", s):
    if len(m.group(2)) < 12:  # 短いラベルのみ（「ロリ」単体系）
        k = m.group(0)[:200]
        if k in seen: continue
        seen.add(k)
        print('GD:', k.replace('\n','\\n'))
        print('---')
# char_loli_ 系の実体
ids = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](char_loli_[a-zA-Z0-9_]*)[\"']", s)))
print('char_loli_ ids:', len(ids), ids[:20])
