"""
現在のファイルで誤って挿入した }]); を元の }, に戻す。
対象: kiroku_E の後に追加された }]); と、そこにある push(
"""
import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# kiroku_E の後の }]); を }, に修正
# パターン: outfits行の後 '  }]);\nwindow.CHAR_TEMPLATES.female.push({\n\n  id:\'char_mahou_youjo_A'
old_bracket = '  }]);\nwindow.CHAR_TEMPLATES.female.push({\n\n  id:\'char_mahou_youjo_A'
new_bracket = '  },\n\n  {\n\n  id:\'char_mahou_youjo_A'
count = content.count(old_bracket)
print("Pattern count:", count)
if count > 0:
    content = content.replace(old_bracket, new_bracket)

# 次のpush→配列区切りへの変換が残っているか確認
# block17の65113付近
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts_iter[17]
lines17 = sc17.group(1).split('\n')
print("65110-65125:")
for j in range(65109, 65126):
    if j < len(lines17): print(j+1, repr(lines17[j][:80]))

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_rb_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
