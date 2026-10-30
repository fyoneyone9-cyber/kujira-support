# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# L22255: rape行の末尾が切れている → !/char_rape_legal_/ と !/char_rape30_/ を補完
# L22257: { key:label:"⚖ 合法レイプ国家"... → 行ごと削除
# L22256: 空行はそのまま

fixed = []
i = 0
while i < len(lines):
    l = lines[i]
    # L22255相当: rapeシリーズで末尾が切れている行を修正
    if "key:'rape'" in l and l.rstrip().endswith('&&'):
        # 次の空行とL22257の壊れた行をスキップして行を補完
        fixed.append("  { key:'rape',     label:\"\\U0001f51e \u30ec\u30a4\u30d7\u30b7\u30ea\u30fc\u30ba\",           match: id => /^char_rape_/.test(id) && !/char_rape_legal_/.test(id) && !/^char_rape30_/.test(id) },\n")
        i += 1
        # 次の空行をスキップ
        if i < len(lines) and lines[i].strip() == '':
            i += 1
        # 壊れたkey:label行をスキップ
        if i < len(lines) and '{ key:label:' in lines[i]:
            i += 1
        # その後の空行もスキップ
        if i < len(lines) and lines[i].strip() == '':
            i += 1
        continue
    fixed.append(l)
    i += 1

# バージョン更新
c_new = ''.join(fixed)
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
for i in range(22248, min(22262, len(lines2))):
    print(f'L{i+1}: {lines2[i].rstrip()[:110]}')
print('Done')
