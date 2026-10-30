# -*- coding: utf-8 -*-
# 幼女・幼児（汎用）系IDと小学生系の全貌確認（巻き込み防止のため厳密プレフィックスで数える）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
pats = ['char_toddler_','char_kindergarten_','char_baby_','char_youchien_',
        'char_loli_daily','char_loli_uniform','char_loli_wafuku','char_loli_fantasy','char_loli_sports','char_loli_idol',
        'char_shougaku_low','char_shougaku_mid','char_shougaku_high','char_shougaku_boy_']
for p in pats:
    ids = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](" + p + r"[a-zA-Z0-9_]*)[\"']", s)))
    print(p, len(ids), ids[:8])
