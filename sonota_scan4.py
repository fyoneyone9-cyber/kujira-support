# -*- coding: utf-8 -*-
# ラベル文字列の生出現位置から近傍のid定義を逆引き（複数行push形式対応）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
kw = ['囚われルシア', '捕食ミア', '産卵ネア', '侵食サラ', '堕落カイ', '白衣のリナ', 'エンタコール', '無乳', '微乳', '普乳', '超巨乳']
found = {}
for t in kw:
    for m in re.finditer(re.escape(t), s):
        i = m.start()
        back = s[max(0, i-600):i]
        ids = re.findall(r"id[\"']?\s*:\s*[\"'](char_[a-zA-Z0-9_]+)[\"']", back)
        if ids:
            found.setdefault(ids[-1], t)
print('found ids:', len(found))
import collections
pref = collections.Counter()
for x in found:
    mm = re.match(r'(char_[a-z0-9]+_[a-z0-9]+)', x)
    pref[mm.group(1) if mm else x] += 1
for k, v in sorted(pref.items()):
    print(' ', k, v)
print('--- sample ---')
for cid, t in sorted(found.items())[:60]:
    print(cid, '|', t)
