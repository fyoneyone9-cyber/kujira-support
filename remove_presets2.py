# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    c = f.read()

# aom3_anime と majicmix_real を配列から除去
old = "[['aom3_anime','\U0001f3a8AOM3\u3010\u30a2\u30cb\u30e1\u3011'],['majicmix_real','\U0001f4f7majic\u3010\u5b9f\u5199\u3011'],"
new = "["
if old in c:
    c = c.replace(old, new)
    print('Removed aom3 and majic from preset array')
else:
    # 個別に除去
    c = c.replace("['aom3_anime','\U0001f3a8AOM3\u3010\u30a2\u30cb\u30e1\u3011'],", '')
    c = c.replace("['majicmix_real','\U0001f4f7majic\u3010\u5b9f\u5199\u3011'],", '')
    print('Removed individually')

# バージョン更新
m = re.search(r'<meta name=["\']version["\'] content=["\'](\d+)["\']', c)
if m:
    old_ver = m.group(1)
    new_ver = str(int(old_ver) + 1)
    c = c.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f'Version: {old_ver} -> {new_ver}')

with open(r'C:\AI\ComfyUI\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('Saved.')

# 確認
with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    c2 = f.read()
lines = [l for l in c2.split('\n') if 'aom3_anime' in l or 'majicmix_real' in l]
print(f'Remaining occurrences: {len(lines)}')
for l in lines[:3]:
    print(' ', l.strip()[:150])
