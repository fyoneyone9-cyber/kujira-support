"""
覚醒剤S1 tifa/aerith の scene 00「炙り」の空間指定を修正
lighter flame under foil → ライターが股間に生える問題
"""
import sys, re, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

OLD_SCENE = (
    "holding aluminum foil,heating drug crystal on foil,"
    "lighter flame under foil,white smoke rising,"
    "inhaling smoke through straw,drug paraphernalia,"
    "dazed expression starting,flushed cheeks beginning,"
    "upper body,dim room,eye level"
)

NEW_SCENE = (
    "holding aluminum foil with both hands at chest level,"
    "drug crystal on foil held in hands,"
    "lighter held beneath foil in hands,"
    "lighter flame heating foil from below in hands,"
    "white smoke rising upward from foil,"
    "face leaning toward smoke,inhaling through straw,"
    "foil held at waist to chest height,"
    "drug paraphernalia in hands,"
    "dazed expression starting,flushed cheeks beginning,"
    "upper body shot,dim room,eye level"
)

count = content.count(OLD_SCENE)
print(f"Found: {count} occurrences")

if count == 0:
    # 部分一致で確認
    print("Trying partial match...")
    partial = "lighter flame under foil"
    idxs = [i for i in range(len(content)) if content[i:i+len(partial)] == partial]
    print(f"  'lighter flame under foil' at: {idxs[:5]}")
    # 各箇所の文脈確認
    for idx in idxs[:3]:
        print(f"  context: {content[idx-50:idx+80]!r}")
else:
    backup = r'C:\AI\ComfyUI\dashboard_backup_scene00fix_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html'
    shutil.copy2(path, backup)
    print(f"Backup: {backup}")
    new_content = content.replace(OLD_SCENE, NEW_SCENE)
    # バージョン更新
    ver_m = re.search(r'content="(\d{10,})"', new_content)
    if ver_m:
        old_ver = ver_m.group(1)
        new_ver = str(int(old_ver) + 1)
        new_content = new_content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
        print(f"Version: {old_ver} -> {new_ver}")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Fixed {count} occurrences")
