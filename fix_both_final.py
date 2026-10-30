import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

# === Block17: 65061行の単独 } を }, に変える ===
sc17 = scripts_iter[17]
inner17 = sc17.group(1)
lines17 = inner17.split('\n')
if lines17[65060].strip() == '}':
    lines17[65060] = '},'
    print("Block17 line 65061: } -> },")
else:
    print("Block17 line 65061:", repr(lines17[65060]))
new17 = '\n'.join(lines17)
content = content[:sc17.start(1)] + new17 + content[sc17.end(1):]

# === Block22: 382-386行の "});\n\n,\n\n{" パターンを "});\nwindow.CHAR_TEMPLATES.female.push({" に ===
scripts_iter2 = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc22 = scripts_iter2[22]
inner22 = sc22.group(1)
lines22 = inner22.split('\n')

# 381-386行確認後修正
print("Block22 lines 380-390:")
for j in range(379, 392):
    if j < len(lines22): print(j+1, repr(lines22[j][:80]))

# "});\n\n,\n\n{" を "});\nwindow.CHAR_TEMPLATES.female.push({" に
# lines22[381]='});', [382]='', [383]=',', [384]='', [385]='{'
if len(lines22) > 386 and lines22[381].strip() == '});' and lines22[383].strip() == ',' and lines22[385].strip() == '{':
    lines22[381] = '});'
    lines22[382] = 'window.CHAR_TEMPLATES.female.push({'
    lines22[383] = ''  # コンテンツはそのまま(lines22[385]以降)
    lines22[384] = ''
    lines22[385] = ''  # { は消す
    print("Block22 fixed });\n,\n{ pattern")
else:
    # 別パターンを検索
    for j in range(370, 400):
        if j < len(lines22) and lines22[j].strip() == ',':
            prev = lines22[j-2].strip() if j >= 2 else ''
            nxt = lines22[j+2].strip() if j+2 < len(lines22) else ''
            if prev.endswith('});') or prev.endswith('}):') or prev == '});':
                if nxt.startswith('{') or nxt == '{':
                    print(f"Found ,  at line {j+1}, replacing with push({{")
                    lines22[j] = 'window.CHAR_TEMPLATES.female.push({'
                    # 次の空行 + { を消す
                    if j+2 < len(lines22) and lines22[j+2].strip() == '{':
                        lines22[j+2] = ''
                    break

new22 = '\n'.join(lines22)
content = content[:sc22.start(1)] + new22 + content[sc22.end(1):]

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_bf_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
