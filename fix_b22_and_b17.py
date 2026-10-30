import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

# Block22: '}\nwindow.CHAR_TEMPLATES.female.push({' → '});\nwindow.CHAR_TEMPLATES.female.push({'
sc22 = scripts_iter[22]
inner22 = sc22.group(1)
old22 = '}\nwindow.CHAR_TEMPLATES.female.push({'
new22 = '});\nwindow.CHAR_TEMPLATES.female.push({'
count22 = inner22.count(old22)
print("Block22: bare } before push count:", count22)
inner22 = inner22.replace(old22, new22)
content = content[:sc22.start(1)] + inner22 + content[sc22.end(1):]

# Block17: 残っている push -> 配列形式変換
scripts_iter2 = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts_iter2[17]
inner17 = sc17.group(1)
old17 = '\nwindow.CHAR_TEMPLATES.female.push({'
count17 = inner17.count(old17)
print("Block17: remaining push count:", count17)
# block17内の push は全部配列形式に
inner17 = inner17.replace(old17, '\n\n  {')
content = content[:sc17.start(1)] + inner17 + content[sc17.end(1):]

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_b22b17_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
