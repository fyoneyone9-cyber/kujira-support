"""
block17 を元バックアップから復元し、
kiroku_B〜E の push() 形式部分だけを配列要素として追加する
"""
import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
orig_path = r'C:\AI\ComfyUI\dashboard_backup_20261020_074027.html'

with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
with open(orig_path, encoding='utf-8', errors='replace') as f:
    orig_content = f.read()

scripts_orig = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', orig_content, re.DOTALL | re.IGNORECASE))
scripts_curr = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

# block17を元から復元
sc17_orig_inner = scripts_orig[17].group(1)
sc17_curr = scripts_curr[17]

content = content[:sc17_curr.start(1)] + sc17_orig_inner + content[sc17_curr.end(1):]
print("Block17 restored from backup")

# kiroku_B〜E は元バックアップのblock17にあるので復元完了
# fix_broad.pyで追加されたキャラ群はblock22にあるのでblock17には不要
# (fix_broad.pyはblock22の push形式を修正するもので、block17には触らない)

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_b17restore_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
    r = subprocess.run(['node', '--check', tmp.name], capture_output=True, timeout=20)
    os.unlink(tmp.name)
    err = r.stderr.decode('utf-8', errors='replace') if r.stderr else ''
    if r.returncode != 0:
        errors.append((i, err))
print("JS errors:", len(errors))
for i, err in errors[:5]:
    print("  block", i, ":", err[:200])
