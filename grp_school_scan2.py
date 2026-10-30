# -*- coding: utf-8 -*-
# 対象グループのfnパターンとID実体数を調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
keys = ['gakurei','youjo_gen','youjo','shogaku','zukan_all','hoken','hoken_tent','hoken_pe_general','hoken_pe_sailor','hoken_pe_ff','shuukyou_s1']
for k in keys:
    for m in re.finditer(r"key:\s*'" + k + r"',\s*label:\s*[\"'][^\"']*[\"'],\s*(?:fn|match)[^\n]{0,200}", s):
        print(k, '=>', m.group(0)[:220].replace('\n','\\n'))
        print('---')
print('=== id counts ===')
pats = ['char_gakurei_','char_youjo_','char_shogaku_','char_shougaku_','char_zukan_','char_hoken_','char_hoken_tent_','char_hoken_pe_','char_shuukyou_','char_tent_hoken_']
for p in pats:
    ids = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](" + p + r"[a-zA-Z0-9_]*)[\"']", s)))
    print(p, len(ids), ids[:6])
