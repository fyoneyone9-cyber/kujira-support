# -*- coding: utf-8 -*-
# char_pov_ 配下のIDプレフィックス内訳とoutfits_ref、GD定義の実フォーマット、POV以外に巻き込むIDがないか確認
import re, sys, io, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
ids = re.findall(r"id:\s*['\"](char_pov_[a-zA-Z0-9_]+)['\"]", s)
print('char_pov_ ids total:', len(ids))
pref = collections.Counter('_'.join(x.split('_')[:3]) for x in ids)
for k, v in sorted(pref.items()):
    print(' ', k, v)
# push形式の確認（単一行 or 複数行）
i = s.find("id:'char_pov_")
print(repr(s[max(0,i-120):i+150]))
print('===')
# outfits_ref
rows = re.findall(r"id:\s*['\"](char_pov_[a-zA-Z0-9_]+)['\"][^\n]*?outfits_ref:\"(S\d+)\"", s)
refs = sorted(set(b for _, b in rows))
print('refs:', refs, 'count with ref:', len(rows))
# GD定義フォーマット
for key in ['pov_normal', 'pov_sailor']:
    j = s.find("key:'" + key + "'")
    print(key, '->', repr(s[max(0,j-30):j+200]))
    print('---')
# hyoi pov（巻き込み注意）
print('hyoi pov:', re.findall(r"char_hyoi_[a-zA-Z0-9_]*pov[a-zA-Z0-9_]*", s)[:3])
