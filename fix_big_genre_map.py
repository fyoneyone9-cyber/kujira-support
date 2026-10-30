# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 'legal':'...' を削除（rape_legalの 'rape_' 部分が消えた残骸）
# _GP_BIG_GENRE_MAP 内の 'legal': エントリを削除
# パターン: ,'legal':'xxx' または 'legal':'xxx',
before = c.count("'legal':")
c_new = re.sub(r",\s*'legal':'[^']*'", '', c)
c_new = re.sub(r"'legal':'[^']*',?\s*", '', c_new)
after = c_new.count("'legal':")
print(f"'legal': entries: {before} -> {after}")

# バージョン更新
m = re.search(r'<meta name=["\']version["\'] content=["\'](\d+)["\']', c_new)
if m:
    old_ver = m.group(1)
    new_ver = str(int(old_ver) + 1)
    c_new = c_new.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f'Version: {old_ver} -> {new_ver}')

with open(r'C:\AI\ComfyUI\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(c_new)
print('Done')
