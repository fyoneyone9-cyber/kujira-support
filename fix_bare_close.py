import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc22 = scripts_iter[22]
lines22 = sc22.group(1).split('\n')
print("Block22 717-730:")
for j in range(716, 731):
    if j < len(lines22): print(j+1, repr(lines22[j][:100]))

# 722行 (index 721): } が単独 → }); に変換
if lines22[721].strip() == '}':
    lines22[721] = '});'
    print("Fixed bare } at 722 -> });")

# 全て: } 単独行で前がoutfitsやpatternsの場合 → });
fixed = 0
for j in range(len(lines22)):
    if lines22[j].strip() == '}':
        prev = ''
        for k in range(j-1, max(0, j-4), -1):
            if lines22[k].strip():
                prev = lines22[k].strip()
                break
        nxt = ''
        for k in range(j+1, min(len(lines22), j+4)):
            if lines22[k].strip():
                nxt = lines22[k].strip()
                break
        if ('outfits' in prev or 'patterns' in prev or 'neg:' in prev or 'prompt:' in prev) and \
           (nxt.startswith('window.') or nxt.startswith('//') or nxt == ''):
            lines22[j] = '});'
            fixed += 1
print("Fixed additional bare } -> }):", fixed)

new22 = '\n'.join(lines22)
content = content[:sc22.start(1)] + new22 + content[sc22.end(1):]
ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_bc2_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
