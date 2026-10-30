# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    c = f.read()

# push()形式（改行あり・outfits_ref形式も含む）
pattern_char = re.compile(
    r'window\.CHAR_TEMPLATES\.female\.push\(\{.*?id:["\']char_rape_legal_[^"\']*["\'].*?\}\);?\n?',
    re.DOTALL
)
matches = pattern_char.findall(c)
print(f'Found {len(matches)} remaining char definitions')
for m in matches[:3]:
    print(f'  {m[:100]}')
c_new = pattern_char.sub('', c)

# CHAR_CATEGORIES の rape_legal エントリ
pattern_cat = re.compile(r'\{\s*key:["\']rape_legal["\'][^}]*\},?\n?')
n = len(pattern_cat.findall(c_new))
print(f'CHAR_CATEGORIES entries: {n}')
c_new = pattern_cat.sub('', c_new)

# バージョン更新
m = re.search(r'<meta name=["\']version["\'] content=["\'](\d+)["\']', c_new)
if m:
    old_ver = m.group(1)
    new_ver = str(int(old_ver) + 1)
    c_new = c_new.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f'Version: {old_ver} -> {new_ver}')

with open(r'C:\AI\ComfyUI\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(c_new)
print('Saved.')

# 仕様書テキストやNOMALE_PREFIXESのrape_legal参照は残置（表示に無影響）
remaining_chars = len(re.findall(r"id:['\"]char_rape_legal_", c_new))
print(f'Remaining char id definitions: {remaining_chars}')
