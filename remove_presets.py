# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 削除対象の<option>タグ
targets = [
    '<option value="aom3_anime">&#x1F3A8; AOM3 \u30a2\u30cb\u30e1\u7cfb (SD1.5 LoRA\u5b66\u7fd2\u30d9\u30fc\u30b9)</option>',
    '<option value="majicmix_real">&#x1F4F7; majicmix \u30ea\u30a2\u30eb\u7cfb (SD1.5 LoRA\u5b66\u7fd2\u30d9\u30fc\u30b9)</option>',
]

removed = 0
for t in targets:
    if t in c:
        c = c.replace(t, '')
        removed += 1
        print(f'Removed: {t[:60]}')
    else:
        print(f'NOT FOUND: {t[:60]}')

if removed > 0:
    # バージョン更新
    import re as re2
    m = re2.search(r'<meta name=["\']version["\'] content=["\'](\d+)["\']', c)
    if m:
        old_ver = m.group(1)
        new_ver = str(int(old_ver) + 1)
        c = c.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
        print(f'Version: {old_ver} -> {new_ver}')

    with open(r'C:\AI\ComfyUI\dashboard.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print('Saved.')
