# -*- coding: utf-8 -*-
import sys, re, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8')

src = r'C:\AI\ComfyUI\dashboard.html'
bak = src + '.bak_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy2(src, bak)
print(f'Backup: {bak}')

with open(src, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. push()形式のキャラ定義を削除（char_rape_legal_ IDを持つもの）
pattern_char = re.compile(
    r'window\.CHAR_TEMPLATES\.female\.push\(\{[^}]*?id:\s*["\']char_rape_legal_[^"\']*["\'][^}]*?\}\);?\n?',
    re.DOTALL
)
matches = pattern_char.findall(c)
print(f'Found {len(matches)} char definitions to remove')
for m in matches[:3]:
    print(f'  sample: {m[:80]}')
c_new = pattern_char.sub('', c)

# 2. CHAR_GROUP_DEFS / CHAR_CATEGORIES / CHAR_CATEGORY_GROUPS の rape_legal エントリ削除
# {key:'rape_legal', ...} 形式
pattern_gd = re.compile(r'\{key:["\']rape_legal["\'][^}]*\},?\n?')
n_gd = len(pattern_gd.findall(c_new))
print(f'Found {n_gd} CHAR_GROUP_DEFS entries')
c_new = pattern_gd.sub('', c_new)

# cats[] 内の 'rape_legal' 文字列エントリ
pattern_cats = re.compile(r"['\"]rape_legal['\"],?\s*")
n_cats = len(pattern_cats.findall(c_new))
print(f'Found {n_cats} cats[] entries')
c_new = pattern_cats.sub('', c_new)

# 3. registerGenre形式があれば削除
pattern_rg = re.compile(r"registerGenre\(\{[^}]*?key:['\"]rape_legal['\"][^}]*?\}\);?\n?", re.DOTALL)
n_rg = len(pattern_rg.findall(c_new))
print(f'Found {n_rg} registerGenre entries')
c_new = pattern_rg.sub('', c_new)

# 4. バージョン更新
m = re.search(r'<meta name=["\']version["\'] content=["\'](\d+)["\']', c_new)
if m:
    old_ver = m.group(1)
    new_ver = str(int(old_ver) + 1)
    c_new = c_new.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f'Version: {old_ver} -> {new_ver}')

with open(src, 'w', encoding='utf-8') as f:
    f.write(c_new)
print('Saved.')

# 確認
remaining = len(re.findall(r'char_rape_legal_', c_new))
print(f'Remaining char_rape_legal_ refs: {remaining}')
