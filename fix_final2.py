import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# Fix1: });, → });
count1 = content.count('});,')
content = content.replace('});,', '});')
print("Fixed });, -> }); :", count1)

# Fix2: } + \nwindow.CHAR_TEMPLATES.female.push({ (no ); between)
# 残りのorphan: } の後に ); なしで push( が来るパターン
# "}\nwindow.CHAR_TEMPLATES.female.push({" → "});\nwindow.CHAR_TEMPLATES.female.push({"
pattern = r'\}\n(window\.CHAR_TEMPLATES\.female\.push\()'
replacement = r'});\n\1'
new_content, count2 = re.subn(pattern, replacement, content)
# 誤置換防止: });\n が ));... にならないように。push( → push(でOK
content = new_content
print("Fixed orphan push:", count2)

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print(f"Version: {old_ver} -> {new_ver}")

shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_final2_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")

# JS構文チェック
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
errors = []
for i, sc in enumerate(scripts):
    sc2 = sc.strip()
    if not sc2 or len(sc2) < 20: continue
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
    tmp.write(sc2); tmp.close()
    r = subprocess.run(['node', '--check', tmp.name], capture_output=True, text=True, timeout=15)
    os.unlink(tmp.name)
    if r.returncode != 0:
        errors.append((i, r.stderr[:200]))
print(f"Remaining JS errors: {len(errors)}")
for i, err in errors[:5]:
    print(f"  block {i}: {err[:150]}")
