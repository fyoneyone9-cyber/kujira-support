"""
block17内の 'const CHAR_TEMPLATES = { female: [], male: [] };' を
'window.CHAR_TEMPLATES = window.CHAR_TEMPLATES || { female: [], male: [] };'
に修正する。
"""
import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'

with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

old = 'const CHAR_TEMPLATES = { female: [], male: [] };'
new = 'window.CHAR_TEMPLATES = window.CHAR_TEMPLATES || { female: [], male: [] };'

count = content.count(old)
print('Found:', count)
if count == 0:
    print('Already fixed or not found.')
    sys.exit(0)

content = content.replace(old, new)

# バージョン更新
ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)

ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_constfix_' + ts + '.html')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")

# JS検証
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
errors = []
for i, sc in enumerate(scripts):
    sc2 = sc.strip()
    if not sc2 or len(sc2) < 20: continue
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
    tmp.write(sc2); tmp.close()
    r = subprocess.run(['node', '--check', tmp.name], capture_output=True, timeout=30)
    os.unlink(tmp.name)
    if r.returncode != 0:
        errors.append((i, r.stderr.decode('utf-8', errors='replace')))
print("JS errors:", len(errors))
for i, e in errors[:3]: print("  block", i, ":", e[:200])
if not errors: print("SUCCESS!")
