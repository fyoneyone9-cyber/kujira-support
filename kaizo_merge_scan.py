# -*- coding: utf-8 -*-
# 改造系グループ定義（画像範囲）の全箇所を調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()

targets = ['医療改造','改造AKB','改造FF','改造JK','改造アニメ','改造エヴァ','改造セーラー','改造その後','改造ダイ','改造鬼滅','改造芸能人']
# GD形式 {key:'x',label:"...",fn:id => /^.../.test(id)},
for m in re.finditer(r"\{key:'([^']+)',label:\"([^\"]+)\",fn:id => ([^}]+)\},", s):
    lab = m.group(2)
    if any(t in lab for t in targets):
        print('GD:', m.group(1), '|', lab, '|', m.group(3)[:100])
print('=== other structures ===')
# CHAR_CATEGORIES形式 match:
for m in re.finditer(r"\{\s*key:\s*'([^']+)',\s*label:\s*'([^']+)',\s*match:", s):
    if any(t in m.group(2) for t in targets):
        print('CAT:', m.group(1), '|', m.group(2))
