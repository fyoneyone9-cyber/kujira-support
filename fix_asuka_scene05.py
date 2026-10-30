import sys, re, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8')

DASHBOARD = r'C:\AI\ComfyUI\dashboard.html'

with open(DASHBOARD, encoding='utf-8', errors='replace') as f:
    content = f.read()

# scene05のvalue（05「鏡を…見せないで」）を確認・置換
# 現在値の最初の部分で特定
OLD_VAL = '"(full body mirror:2.0),(post-surgery body:1.9),(body modification visible:1.8),(horror:1.8),(covering'
if OLD_VAL not in content:
    # 前後確認
    idx = content.find('full body mirror:2.0')
    if idx > 0:
        print(repr(content[idx-2:idx+200]))
    else:
        print("NOT FOUND")
    sys.exit()

# 元のvalueを探して全体を取得
idx = content.find(OLD_VAL)
end = content.find('"', idx + len(OLD_VAL))
# valueの閉じダブルクォートを探す（エスケープなし）
full_val_end = idx
depth = 0
for i in range(idx, idx+500):
    if content[i] == '"' and content[i-1] != '\\':
        if i == idx:
            continue
        full_val_end = i
        break

old_full = content[idx:full_val_end+1]
print("OLD:", old_full[:150])

NEW_VAL = ('"(large floor mirror:2.2),(full body mirror:2.0),(reflection in mirror:1.9),'
           '(post-surgery body:1.9),(body modification visible:1.8),(hospital room:1.7),'
           '(horror at reflection:1.9),(covering face with hands:1.8),(tears:1.7),'
           '(standing in front of mirror:1.8),(full body shot:1.6)"')

shutil.copy2(DASHBOARD, DASHBOARD.replace('.html', f'_backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.html'))
content = content.replace(old_full, NEW_VAL, 1)

# バージョン更新
ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1)
    content = content.replace(f'content="{old_ver}"', f'content="{int(old_ver)+1}"', 1)
    print(f'version: {old_ver} -> {int(old_ver)+1}')

with open(DASHBOARD, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
