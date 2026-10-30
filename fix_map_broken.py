# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    c = f.read()

before = c.count(",:'")
# ,:'xxx' パターン（キーが空）を削除
c_new = re.sub(r",\s*:\s*'[^']*'", '', c)
after = c_new.count(",:'")
print(f"Broken ,:'...' entries: {before} -> {after}")

# バージョン更新
m = re.search(r"name=['\"]version['\"] content=['\"](\d+)['\"]", c_new)
if m:
    old_ver = m.group(1)
    new_ver = str(int(old_ver) + 1)
    c_new = c_new.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f'Version: {old_ver} -> {new_ver}')

with open(r'C:\AI\ComfyUI\dashboard.html','w',encoding='utf-8') as f:
    f.write(c_new)
print('Saved.')
