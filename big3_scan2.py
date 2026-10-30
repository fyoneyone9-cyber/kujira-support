# -*- coding: utf-8 -*-
# 学年・職業（先生）グループと、各IDパターンの実体数を調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
# 学年・職業 bigGenre
for m in re.finditer(r"\{key:'([^']+)',label:\"([^\"]*)\",fn:id => ([^\n]*?),bigGenre:'([^']*(?:学年|職業)[^']*)'\},", s):
    print('GD:', m.group(1), '|', m.group(2), '|', m.group(3)[:80], '|', m.group(4))
# 先生ラベル
for m in re.finditer(r"key:\s*'([^']+)',\s*label:\s*[\"']([^\"']*先生[^\"']*)[\"']", s):
    print('SENSEI:', m.group(1), '|', m.group(2))
print('=== id counts ===')
pats = ['char_ff_', 'char_ff7_', 'char_ff8_', 'char_ff10_', 'char_ff13_', 'char_sailor_', 'char_tuxedo', 'char_incubus_', 'char_kimetsu_',
        'char_cp_', 'char_loracheck_', 'char_anime_', 'char_celeb_', 'char_akb_', 'char_ske_', 'char_heroine_', 'char_chibi_moon2',
        'char_legal_eva_', 'char_legal_sailor_', 'char_legal_ff_', 'char_legal_kimetsu_', 'char_sensei', 'char_teacher']
for p in pats:
    ids = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](" + p + r"[a-zA-Z0-9_]*)[\"']", s)))
    print(p, len(ids), ids[:6])
