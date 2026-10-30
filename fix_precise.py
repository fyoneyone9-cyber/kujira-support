import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

# === Block17 fix: char_nyuuji_C が unclosed → push({ の前に } を追加 ===
sc17 = scripts_iter[17]
inner17 = sc17.group(1)
lines17 = inner17.split('\n')
# kiroku_B の前の push({ を探す
for j, l in enumerate(lines17):
    if 'char_kiroku_B' in l:
        kiroku_b_line = j
        break
# kiroku_B の push({ の行
for j in range(kiroku_b_line, max(0, kiroku_b_line-10), -1):
    if 'CHAR_TEMPLATES.female.push({' in lines17[j]:
        push_line = j
        break
# push_line の前の空行を探して } を挿入
prev_non_empty = push_line - 1
while prev_non_empty > 0 and lines17[prev_non_empty].strip() == '':
    prev_non_empty -= 1
print(f"Block17: push at line {push_line+1}, prev non-empty at {prev_non_empty+1}:", repr(lines17[prev_non_empty][:80]))
# prev_non_empty の行がoutfitsの末尾またはcloseでない場合、push_lineの直前に } を挿入
if not lines17[prev_non_empty].strip().startswith('}'):
    lines17.insert(push_line, '}')
    print("  Inserted } before push")
else:
    print("  Already has }, skip")
new_inner17 = '\n'.join(lines17)
content = content[:sc17.start(1)] + new_inner17 + content[sc17.end(1):]

# === Block22 fix: ); の後に , が残っている ===
scripts_iter2 = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc22 = scripts_iter2[22]
inner22 = sc22.group(1)
# ]);, または });, を修正
count_a = inner22.count(']);,')
count_b = inner22.count('});,')
inner22 = inner22.replace(']);,', ']);').replace('});,', '});')
print("Block22: fixed ]);, x", count_a, "and });, x", count_b)
content = content[:sc22.start(1)] + inner22 + content[sc22.end(1):]

# === バージョン・保存 ===
ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_prec_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
