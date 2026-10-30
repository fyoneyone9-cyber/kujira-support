# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

out = []
skip = False
removed = 0
i = 0
while i < len(lines):
    l = lines[i]
    # push開始行でchar_rape_legal_を含む
    if 'window.CHAR_TEMPLATES.female.push' in l and 'char_rape_legal_' in l:
        skip = True
        removed += 1
    if skip:
        # });で終わる行まで読み飛ばす
        if l.rstrip().endswith(');') or l.rstrip().endswith(');'):
            skip = False
        i += 1
        continue
    out.append(l)
    i += 1

print(f'Removed {removed} push() blocks')

# cats[]内のrape_legal文字列
out2 = []
for l in out:
    if "'rape_legal'" in l or '"rape_legal"' in l:
        # cats配列内のエントリのみ削除
        if 'cats' in l or 'key' in l:
            l = l.replace("'rape_legal',", "").replace('"rape_legal",', "")
    out2.append(l)

# バージョン更新
import re
c_new = ''.join(out2)
m = re.search(r'<meta name=["\']version["\'] content=["\'](\d+)["\']', c_new)
if m:
    old_ver = m.group(1)
    new_ver = str(int(old_ver) + 1)
    c_new = c_new.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f'Version: {old_ver} -> {new_ver}')

with open(r'C:\AI\ComfyUI\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(c_new)

# 確認
remaining = c_new.count("id:'char_rape_legal_") + c_new.count('id:"char_rape_legal_')
print(f'Remaining char_rape_legal_ id defs: {remaining}')
print('Done')
