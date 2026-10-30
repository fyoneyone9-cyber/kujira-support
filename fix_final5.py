import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

# Block17: kiroku_B push が65062から始まり65072でoutfitsが終わり、次のkiroku_C pushが65075
# 65073,65074が空行 → 65073に '});' を追加
sc17 = scripts_iter[17]
inner17 = sc17.group(1)
lines17 = inner17.split('\n')
# 65073,65074 が空で 65075が push
if lines17[65074].strip() == 'window.CHAR_TEMPLATES.female.push({' and lines17[65073].strip() == '':
    lines17[65073] = '});'
    print("Block17: Added }); at line 65074")
else:
    print("Block17 65075:", repr(lines17[65074]))
content = content[:sc17.start(1)] + '\n'.join(lines17) + content[sc17.end(1):]

# Block22: 491行 }); のエラーを確認・修正
scripts_iter2 = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc22 = scripts_iter2[22]
inner22 = sc22.group(1)
lines22 = inner22.split('\n')
print("\nBlock22 487-498:")
for j in range(486, 499):
    if j < len(lines22): print(j+1, repr(lines22[j][:100]))

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_f5_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
