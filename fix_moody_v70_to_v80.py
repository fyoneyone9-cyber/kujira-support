import sys, io, pathlib, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

V70 = "moodyKrea2MixUncensoredWeekend_v70_fp8"
V80 = "moodyKrea2MixUncensoredV8SEGoes_v80_int8"

DASHBOARD = pathlib.Path(r"C:\AI\ComfyUI\dashboard.html")

# バックアップ
import shutil
bak = DASHBOARD.parent / (DASHBOARD.name + ".bak_v70fix")
shutil.copy2(DASHBOARD, bak)
print(f"Backup: {bak}")

with open(DASHBOARD, encoding='utf-8', errors='replace') as f:
    content = f.read()

old_count = content.count(V70)
print(f"V70 occurrences before: {old_count}")

new_content = content.replace(V70, V80)

new_count = new_content.count(V70)
print(f"V70 occurrences after: {new_count}")
print(f"V80 occurrences: {new_content.count(V80)}")

if old_count > 0 and new_count == 0:
    # バージョン番号を更新
    import re as re_v
    ver_match = re_v.search(r'content="(\d{10})"', new_content)
    if ver_match:
        old_ver = ver_match.group(1)
        new_ver = str(int(old_ver) + 1)
        new_content = new_content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
        print(f"Version: {old_ver} -> {new_ver}")
    
    with open(DASHBOARD, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("✅ dashboard.html updated")
else:
    print("❌ 置換に問題があります。変更を保存しませんでした。")
