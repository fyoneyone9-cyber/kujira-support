import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc22 = scripts_iter[22]
lines22 = sc22.group(1).split('\n')

# 1732行周辺確認
print("Block22 1726-1738:")
for j in range(1725, 1739):
    if j < len(lines22): print(j+1, repr(lines22[j][:100]))

# label: の前のid行/push欠けを確認・修正
# 全block22をスキャンして push欠けのパターンを探す
# パターン: '});' の後に id: か label: で始まる行
fixed = 0
for j in range(1, len(lines22)):
    l = lines22[j].strip()
    if l.startswith("id:'char_") or l.startswith('id:"char_') or l.startswith("id: 'char_"):
        prev = ''
        for k in range(j-1, max(0,j-5), -1):
            if lines22[k].strip():
                prev = lines22[k].strip()
                break
        if prev not in ('window.CHAR_TEMPLATES.female.push({', '{') and not prev.endswith(','):
            # pushが必要
            lines22.insert(j, 'window.CHAR_TEMPLATES.female.push({')
            fixed += 1
            print(f"Inserted push before id at {j+1}")
print("Total push inserted:", fixed)

new22 = '\n'.join(lines22)
content = content[:sc22.start(1)] + new22 + content[sc22.end(1):]
ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_1732_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
