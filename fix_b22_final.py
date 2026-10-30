import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc22 = scripts_iter[22]
lines22 = sc22.group(1).split('\n')
print("Block22 240-252:")
for j in range(239, 253): print(j+1, repr(lines22[j][:100]))

# 245行 (index 244) の前後を確認
# id: の前に push が必要 → 242-244を確認してpush追加
# 242行に }); があれば次のchar用にpush追加
for j in range(240, 248):
    l = lines22[j].strip()
    if l.startswith("id:'char_rohypnol_jk_A'"):
        # 直前に push が必要
        prev = lines22[j-1].strip() if j > 0 else ''
        print(f"  line {j+1} id found, prev: {repr(prev)}")
        if prev == '':
            prev2 = lines22[j-2].strip() if j > 1 else ''
            print(f"  line {j}: {repr(prev2)}")
            if prev2 in ('});', '}'):
                # push を j-1に挿入
                lines22.insert(j, 'window.CHAR_TEMPLATES.female.push({')
                print("  Inserted push({ before id line")
        break

new22 = '\n'.join(lines22)
content = content[:sc22.start(1)] + new22 + content[sc22.end(1):]

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_b22f_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
