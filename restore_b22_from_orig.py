"""
block22 を元バックアップから復元し、
その後に add_all_chars.py / add_s3_chars.py / fix_s1_outfits.py / fix_s2s3_outfits.py
で追加したキャラ群を正しく再追加する
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

# block22を元から復元
sc22_orig_inner = scripts_orig[22].group(1)
sc22_curr = scripts_curr[22]
content = content[:sc22_curr.start(1)] + sc22_orig_inner + content[sc22_curr.end(1):]
print("Block22 restored from backup")

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_b22restore_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
