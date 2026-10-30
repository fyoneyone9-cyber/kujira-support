# -*- coding: utf-8 -*-
# 改造版権v2 10グループのID実体数と形式確認（kaizou_ff/kaizou_kimetsu/kaizou_sailor旧グループは対象外）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
pats = ['char_kaizo_akb_', 'char_kaizo_ff_', 'char_kaizo_anime_', 'char_kaizo_eva_', 'char_kaizo_sailor_',
        'char_kaizo_dai_', 'char_kaizo_kimetsu_', 'char_kaizo_celeb_', 'char_kaizo_rei', 'char_kaizo_emma']
tot = set()
for p in pats:
    ids = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](" + p + r"[a-zA-Z0-9_]*)[\"']", s)))
    print(p, len(ids), ids[:8])
    tot.update(ids)
print('total unique:', len(tot))
# 巻き込み注意: char_kaizo_nichijou / char_kaizo_singer(削除済) / char_kaizo_jibril(削除済) 等が
# 上記パターンに引っかからないか → プレフィックスが異なるのでOK。kaizo_rei がkaizo_reinaなど拾わないか確認
extra = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](char_kaizo_[a-zA-Z0-9_]*)[\"']", s)))
others = [x for x in extra if x not in tot]
print('other kaizo_ ids (not deleted):', len(others), others[:20])
