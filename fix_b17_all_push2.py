import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts_iter[17]
inner17 = sc17.group(1)

# 全パターン: 任意の空白+});\nwindow.CHAR_TEMPLATES.female.push({ を置換
# → インデント部分を捨てて  }, に
import re as re2
def replace_push_in_array(m):
    indent = m.group(1)  # }) の前の空白
    return indent + '},\n\n' + indent + '{'

pattern = r'([ \t]*)[}][)][;]\nwindow[.]CHAR_TEMPLATES[.]female[.]push[(][{]'
count = len(re2.findall(pattern, inner17))
print(f"Pattern count: {count}")
inner17 = re2.sub(pattern, replace_push_in_array, inner17)

content = content[:sc17.start(1)] + inner17 + content[sc17.end(1):]

ver_m = re2.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_b17p2_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")

scripts = re2.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re2.DOTALL | re2.IGNORECASE)
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
