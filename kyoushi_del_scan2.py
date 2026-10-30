# -*- coding: utf-8 -*-
# S0165/S0168 の共有状況、cosplay pushの形式、GD定義形式を確認
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
for r in ['S0165', 'S0168']:
    users = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](char_[a-zA-Z0-9_]+)[\"'][^\n]*?outfits_ref:\"" + r + r"\"", s)))
    nonc = [u for u in users if not u.startswith('char_cosplay_')]
    print(r, 'users:', len(users), 'non-cosplay:', nonc[:5])
# push形式サンプル
for cid in ['char_cosplay_zukan_aerith', 'char_cosplay_zukan_chuugaku_A', 'char_kyoushi_s1_youjo_a']:
    m = re.search(r"id[\"']?\s*:\s*[\"']" + cid + r"[\"']", s)
    i = m.start()
    print(cid, '||', repr(s[max(0,i-100):i+30])[:170])
    print('---')
# GD定義形式
for m in re.finditer(r"key:\s*'(?:cosplay_zukan|cosplay_zukan_jk|kyoushi_s1)'[^\n]{0,180}", s):
    print('GD:', m.group(0)[:200])
    print('---')
