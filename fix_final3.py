import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

# Block17: 65074行の `  });` を削除
sc17 = scripts_iter[17]
inner17 = sc17.group(1)
lines17 = inner17.split('\n')
print("Block17 line 65074:", repr(lines17[65073]))
if lines17[65073].strip() == '});':
    lines17[65073] = ''
    print("  Removed orphan });")
content = content[:sc17.start(1)] + '\n'.join(lines17) + content[sc17.end(1):]

# Block22: 475行エラーを確認
scripts_iter2 = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc22 = scripts_iter2[22]
inner22 = sc22.group(1)
lines22 = inner22.split('\n')
print("\nBlock22 470-480:")
for j in range(469, 481):
    if j < len(lines22): print(j+1, repr(lines22[j][:120]))

# 1行 {id:'...' (...)} を修正 (endswith } でも push前の  ; で閉じている可能性)
# 458: '{id:\'char_kakuseizai_s2_usagi\'' が push なしかを再確認
print("\nBlock22 455-465:")
for j in range(454, 466):
    if j < len(lines22): print(j+1, repr(lines22[j][:120]))

# 修正: 458-464の {id:'char_ 行に push( を追加（outfitsが1行なら }); で終わる）
for j in range(len(lines22)):
    l = lines22[j]
    stripped = l.lstrip()
    if re.match(r"\{id:'char_", stripped):
        # pushが直前にない
        prev_lines = [lines22[k].strip() for k in range(max(0,j-3), j) if lines22[k].strip()]
        has_push = any('CHAR_TEMPLATES' in p and 'push(' in p for p in prev_lines)
        if not has_push:
            if stripped.endswith('}'):
                lines22[j] = 'window.CHAR_TEMPLATES.female.push(' + stripped + ');'
            elif stripped.endswith('},'):
                lines22[j] = 'window.CHAR_TEMPLATES.female.push(' + stripped[:-1] + ');'
            else:
                lines22[j] = 'window.CHAR_TEMPLATES.female.push(' + stripped
            print(f"  Fixed bare bare {{id at line {j+1}")

new22 = '\n'.join(lines22)
content = content[:sc22.start(1)] + new22 + content[sc22.end(1):]

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_f3_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
