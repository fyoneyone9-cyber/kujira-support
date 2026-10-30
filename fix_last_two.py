import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

# Block17: '  });,{' → '  },' + '{' (空白調整)
sc17 = scripts_iter[17]
inner17 = sc17.group(1)
count17a = inner17.count('  });,{')
inner17 = inner17.replace('  });,{', '  },{')
print("Block17: fixed });,{ x", count17a)

# Block17: '});,\n{' パターンも
count17b = inner17.count('});\n,\n{')
inner17 = inner17.replace('});\n,\n{', '},\n{')
print("Block17: fixed );newline,newline{ x", count17b)

content = content[:sc17.start(1)] + inner17 + content[sc17.end(1):]

# Block22: 213行の { → push({
scripts_iter2 = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc22 = scripts_iter2[22]
lines22 = sc22.group(1).split('\n')
print("Block22 210-218:")
for j in range(209, 219): print(j+1, repr(lines22[j][:80]))
if lines22[212].strip() == '}':
    lines22[212] = 'window.CHAR_TEMPLATES.female.push({'
    print("Block22 213: } -> push({")
content = content[:sc22.start(1)] + '\n'.join(lines22) + content[sc22.end(1):]

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_lt_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
