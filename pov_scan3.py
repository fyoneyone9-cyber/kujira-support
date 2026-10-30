# -*- coding: utf-8 -*-
# POV削除前の詳細調査: push形式の全パターン / GD定義の全箇所 / outfit_refの共有状況
import re, sys, io, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()

# 1) push行の形式確認（単一行で }); まで閉じるか）
pushes = re.findall(r"(?:window\.)?CHAR_TEMPLATES\.female\.push\(\{id:'char_pov_[^']*'.*?\}\);", s)
print('single-line-style pushes:', len(pushes))
multi = re.findall(r"(?:window\.)?CHAR_TEMPLATES\.female\.push\(\{\s*\n+\s*id:\s*['\"]char_pov_", s)
print('multi-line pushes:', len(multi))

# 2) char_pov_ の全出現数
print('char_pov_ total occurrences:', s.count('char_pov_'))

# 3) outfits_ref を持つPOVキャラの ref 一覧と、その ref を使う非POVキャラ数
rows = re.findall(r"id:'(char_pov_[a-zA-Z0-9_]+)'[^\n]*?outfits_ref:\"(S\d+)\"", s)
povrefs = sorted(set(b for _, b in rows))
print('pov refs:', povrefs)
for r in povrefs:
    users = re.findall(r"id:'(char_[a-zA-Z0-9_]+)'[^\n]*?outfits_ref:\"" + r + r"\"", s)
    nonpov = [u for u in users if not u.startswith('char_pov_')]
    print(r, 'users:', len(users), 'non-pov:', len(nonpov), nonpov[:3])

# 4) GDエントリ全箇所（char_pov参照の定義行）数
gd_hits = [m.start() for m in re.finditer(r"key:\s*'(?:pov_[a-z]+|pov|grp_pov|pov_all|cp_all)'", s)]
print('gd key hits:', len(gd_hits))
for i in gd_hits:
    print(repr(s[max(0,i-40):i+160])[:230])
    print('---')
