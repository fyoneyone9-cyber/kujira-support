# -*- coding: utf-8 -*-
# 削除前最終調査: 各IDのpush形式確認、senseiグループ定義、他グループからの参照巻き込み確認
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
samples = ['char_ff_tifa','char_ff7_aerith','char_sailor_moon','char_tuxedo_mask','char_incubus_A','char_kimetsu_nezuko','char_loracheck_bound_tentacle_jk','char_chibi_moon2','char_sensei']
for cid in samples:
    m = re.search(r"id[\"']?\s*:\s*[\"']" + cid + r"[\"']", s)
    i = m.start()
    print(cid, '||', repr(s[max(0,i-110):i+30])[:170])
    print('---')
# sensei_chars GD形式
for m in re.finditer(r"key:\s*'sensei_chars'[^\n]{0,200}", s):
    print('SENSEI GD:', m.group(0)[:220])
    print('---')
# char_sensei が他で使われるか
print('char_sensei occurrences:', s.count('char_sensei'))
