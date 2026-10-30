# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# char_rape_legal_ の id行を含むpushブロックを削除
# ブロックは空行 → push({ 開始 → 空行を含む複数行 → }); で終わる
# 方針: id行の前後で push({ ... }); の範囲を特定して削除

to_delete = set()
i = 0
while i < len(lines):
    if 'char_rape_legal_' in lines[i] and ("id:'" in lines[i] or 'id:"' in lines[i]):
        # この行を含むpushブロックを探す
        # 上方向にpush({を探す
        start = i
        for j in range(i, max(i-5, -1), -1):
            if 'window.CHAR_TEMPLATES.female.push' in lines[j]:
                start = j
                break
        # 下方向に});を探す
        end = i
        for j in range(i, min(i+20, len(lines))):
            if lines[j].rstrip().endswith(');'):
                end = j
                break
        for k in range(start, end+1):
            to_delete.add(k)
        print(f'Delete L{start+1}-L{end+1}: {lines[i].strip()[:60]}')
        i = end + 1
    else:
        i += 1

out = [l for i, l in enumerate(lines) if i not in to_delete]
print(f'Deleted {len(to_delete)} lines')

# バージョン更新
c_new = ''.join(out)
m = re.search(r'<meta name=["\']version["\'] content=["\'](\d+)["\']', c_new)
if m:
    old_ver = m.group(1)
    new_ver = str(int(old_ver) + 1)
    c_new = c_new.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f'Version: {old_ver} -> {new_ver}')

with open(r'C:\AI\ComfyUI\dashboard.html', 'w', encoding='utf-8') as f:
    f.write(c_new)

remaining = c_new.count("id:'char_rape_legal_") + c_new.count('id:"char_rape_legal_')
print(f'Remaining: {remaining}')
print('Done')
