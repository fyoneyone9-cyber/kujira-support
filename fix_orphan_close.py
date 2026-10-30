import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

# block17 の問題: outfits行の後に });  がある（65060行）
# block17 start position in full content
sc17 = scripts_iter[17]
sc17_start = sc17.start(1)  # inner start
sc17_inner = sc17.group(1)
lines17 = sc17_inner.split('\n')

# 65060行(0-indexed: 65059)の "  });" を削除
target_line_idx = 65059
if lines17[target_line_idx].strip() == '});':
    print("Found orphan });" , repr(lines17[target_line_idx]))
    lines17[target_line_idx] = ''  # 削除（空行に）
    new_inner = '\n'.join(lines17)
    content = content[:sc17_start] + new_inner + content[sc17.end(1):]
    print("Removed orphan });" )
else:
    print("Line 65060:", repr(lines17[target_line_idx]))

# block22 の問題確認と修正
scripts_iter2 = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc22 = scripts_iter2[22]
sc22_inner = sc22.group(1)
lines22 = sc22_inner.split('\n')
# 340行付近
print('\nBlock22 around 337-345:')
for j in range(336, 346):
    if j < len(lines22): print(j+1, repr(lines22[j][:120]))

# block22: kakuseizai_chuugaku_A の前に裸の { がある
# 338行付近を確認して修正
for j in range(335, 345):
    if j < len(lines22) and lines22[j].strip() == '{':
        # この { の前行が }); なら push({ に変換
        prev = lines22[j-2].strip() if j >= 2 else ''
        print(f"Bare {{ at line {j+1}, prev2={repr(prev)}")
        lines22[j] = 'window.CHAR_TEMPLATES.female.push({'
        print(f"Fixed to push({{")
        break

new_inner22 = '\n'.join(lines22)
content = content[:sc22.start(1)] + new_inner22 + content[sc22.end(1):]

# バージョン更新・保存
ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_oc_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")

# JS check
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
