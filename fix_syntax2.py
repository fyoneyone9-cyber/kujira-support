# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# L22255とL22257を直接修正（0-indexed: 22254, 22256）
print(f'L22255 repr: {repr(lines[22254][:150])}')
print(f'L22257 repr: {repr(lines[22256][:150])}')

# L22255: 末尾を正しい形に
lines[22254] = "  { key:'rape',     label:\"\U0001f51e \u30ec\u30a4\u30d7\u30b7\u30ea\u30fc\u30ba\",           match: id => /^char_rape_/.test(id) && !/char_rape_legal_/.test(id) && !/^char_rape30_/.test(id) },\n"

# L22257: 壊れた行を削除（空行に）
lines[22256] = "\n"
# L22258: 空行削除
lines[22257] = "\n"

c_new = ''.join(lines)

# バージョン更新
m = re.search(r'<meta name=["\']version["\'] content=["\'](\d+)["\']', c_new)
if m:
    old_ver = m.group(1)
    new_ver = str(int(old_ver) + 1)
    c_new = c_new.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f'Version: {old_ver} -> {new_ver}')

with open(r'C:\AI\ComfyUI\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(c_new)

# 確認
with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    lines2 = f.readlines()
for i in range(22252, 22262):
    print(f'L{i+1}: {lines2[i].rstrip()[:110]}')
print('Done')
