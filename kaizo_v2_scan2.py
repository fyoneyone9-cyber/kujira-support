# -*- coding: utf-8 -*-
# 削除対象6グループのID実体数と形式確認（sekai_duo系は対象外・巻き込み確認）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
pats = ['char_kaizo_jibril_', 'char_kaizo_tifa', 'char_kaizo_2b', 'char_kaizo_miku', 'char_kaizo_singer_', 'char_kaizo_taylor']
tot = set()
for p in pats:
    ids = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](" + p + r"[a-zA-Z0-9_]*)[\"']", s)))
    print(p, len(ids), ids)
    tot.update(ids)
print('total unique:', len(tot))
# 他のkaizo系（kaizo_nichijou等）を巻き込まないか: kaizo_tifaパターンがkaizo_tifaXXXのみか確認
# refs
for cid in sorted(tot):
    m = re.search(r"id[\"']?\s*:\s*[\"']" + cid + r"[\"']", s)
    seg = s[m.start():m.start()+3000]
    r = re.search(r"outfits_ref:[\"'](S\d+)[\"']", seg)
    print(cid, '->', r.group(1) if r else None)
