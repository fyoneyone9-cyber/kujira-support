# -*- coding: utf-8 -*-
# スクショのラベル（囚われルシア/捕食ミア/エンタコール 乳児/無乳 幼女 等）からIDを逆引き
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
kw = ['囚われルシア', '捕食ミア', '産卵ネア', '侵食サラ', '寄生リン', '繭ユウ', '堕落カイ', '融合アン', '産卵シエル',
      '白衣のリナ', 'ピンク頭のマリ', '黒髪のアヤ', 'エンタコール', '無乳', '微乳', '普乳', '巨乳 幼女', '超巨乳']
found = {}
for m in re.finditer(r"id[\"']?\s*:\s*[\"'](char_[a-zA-Z0-9_]+)[\"']\s*,\s*(?:genre[^,]*,)?\s*[\"']?label[\"']?\s*:\s*[\"']([^\"']+)[\"']", s):
    cid, lab = m.group(1), m.group(2)
    if any(t in lab for t in kw):
        found[cid] = lab
print('found:', len(found))
import collections
pref = collections.Counter('_'.join(x.split('_')[:3]) for x in found)
for k, v in sorted(pref.items()):
    print(' ', k, v)
for cid, lab in sorted(found.items())[:100]:
    print(cid, '|', lab[:40])
