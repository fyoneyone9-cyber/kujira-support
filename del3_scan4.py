# -*- coding: utf-8 -*-
# char_tousatsu_ のキャラ定義実体を探す（クォート形式違いに対応）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
# あらゆるクォートでid値を拾う
ids = set(re.findall(r"id:\s*[\"'](char_tousatsu_[a-z0-9_]+)[\"']", s))
print('ids:', len(ids))
for i in sorted(ids):
    print(' ', i)
# 盗撮園児(char_tousatsu_youchien_)は別グループ → 女湯のIDパターン確認
# 定義行の形式確認
for cid in sorted(ids)[:2]:
    j = s.find(cid)
    print(repr(s[max(0,j-150):j+200]))
    print('---')
