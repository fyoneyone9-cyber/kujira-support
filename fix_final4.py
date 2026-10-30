import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

# Block22: 477行の単独 ); を削除
sc22 = scripts_iter[22]
inner22 = sc22.group(1)
lines22 = inner22.split('\n')
print("Block22 474-481:")
for j in range(473, 482):
    if j < len(lines22): print(j+1, repr(lines22[j][:80]))
if lines22[476].strip() == ');':
    lines22[476] = ''
    print("Removed orphan ); at line 477")
new22 = '\n'.join(lines22)
content = content[:sc22.start(1)] + new22 + content[sc22.end(1):]

# Block17: 65073行エラーを確認
scripts_iter2 = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts_iter2[17]
inner17 = sc17.group(1)
lines17 = inner17.split('\n')
print("\nBlock17 65060-65078:")
for j in range(65059, 65079):
    if j < len(lines17): print(j+1, repr(lines17[j][:100]))

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_f4_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")

scripts_final = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
errors = []
for i, sc in enumerate(scripts_final):
    sc2 = sc.strip()
    if not sc2 or len(sc2) < 20: continue
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
    tmp.write(sc2); tmp.close()
    r = subprocess.run(['node', '--check', tmp.name], capture_output=True, timeout=15)
    os.unlink(tmp.name)
    err = r.stderr.decode('utf-8', errors='replace') if r.stderr else ''
    if r.returncode != 0:
        errors.append((i, err))
print("Remaining JS errors:", len(errors))
for i, err in errors[:5]:
    print("  block", i, ":", err[:200])
