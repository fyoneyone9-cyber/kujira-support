"""
rape_nyuuji_Cの後の }]); を  }, に戻し
その後の window.CHAR_TEMPLATES.female.push({ を  { に戻す
（元バックアップの配列形式に戻す）
"""
import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# rape_nyuuji_C の outfits行の後に来る }]); を  }, に変換
# ターゲット: "outfits: [{...}]\n\n}]);\nwindow.CHAR_TEMPLATES"
# パターンで直接置換

old1 = '\n}]);\nwindow.CHAR_TEMPLATES.female.push({'
new1 = '\n  },\n\n  {'
count1 = content.count(old1)
print(f"Pattern 1 count: {count1}")
if count1 > 0:
    content = content.replace(old1, new1, 1)

# 別パターン確認
old2 = '\n});\nwindow.CHAR_TEMPLATES.female.push({'
count2 = content.count(old2)
print("Pattern 2 (" + "});) count:", count2)

# block17内のkiroku_B の push を配列形式に戻す
# 現在: "  },\n\n  {\n\n    id:'char_kiroku_B'" の直前に push があれば削除
# char_kiroku_B の前の { が配列要素になっているか確認
idx = content.find("id:'char_kiroku_B'")
if idx < 0: idx = content.find('id:\'char_kiroku_B\'')
if idx >= 0:
    # 前200文字を確認
    print(repr(content[max(0,idx-200):idx+50]))

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_bc_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")

scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
errors = []
for i, sc in enumerate(scripts):
    sc2 = sc.strip()
    if not sc2 or len(sc2) < 20: continue
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
    tmp.write(sc2); tmp.close()
    r = subprocess.run(['node', '--check', tmp.name], capture_output=True, timeout=15)
    os.unlink(tmp.name)
    err = r.stderr.decode('utf-8', errors='replace') if r.stderr else ''
    if r.returncode != 0:
        errors.append((i, err))
print("JS errors:", len(errors))
for i, err in errors[:5]:
    print("  block", i, ":", err[:200])
