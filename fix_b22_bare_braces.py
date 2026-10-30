"""
block22内の '});' の後に来る裸の '{' を全て 'window.CHAR_TEMPLATES.female.push({' に変換
"""
import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc22 = scripts_iter[22]
inner22 = sc22.group(1)
lines22 = inner22.split('\n')

fixed = 0
i = 0
while i < len(lines22):
    if lines22[i].strip() == '{':
        # 直前に }); か //コメント行があり、次の行が id:'char_... であれば push
        prev_non_empty = ''
        for k in range(i-1, max(0, i-5), -1):
            if lines22[k].strip():
                prev_non_empty = lines22[k].strip()
                break
        next_non_empty = ''
        for k in range(i+1, min(len(lines22), i+5)):
            if lines22[k].strip():
                next_non_empty = lines22[k].strip()
                break
        if next_non_empty.startswith("id:'char_") or next_non_empty.startswith('id:"char_'):
            lines22[i] = 'window.CHAR_TEMPLATES.female.push({'
            fixed += 1
    i += 1
print("Fixed bare { before char_id:", fixed)

new22 = '\n'.join(lines22)
content = content[:sc22.start(1)] + new22 + content[sc22.end(1):]

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_b22bb_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
