import sys, re, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

def extract_object(content, start):
    s = content.find('{', start)
    if s < 0: return None, -1, -1
    depth = 0; in_str = False; sc = None; i = s
    while i < len(content):
        c = content[i]
        if in_str:
            if c == '\\': i += 2; continue
            if c == sc: in_str = False
        else:
            if c in ('"', "'"): in_str = True; sc = c
            elif c == '{': depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0: return content[s:i+1], s, i+1
        i += 1
    return None, -1, -1

# 全壊れパターンを検索
broken_positions = [(m.start(), m.group(1)) for m in re.finditer(r"\},\n\{\n  id:'(char_kakuseizai_[^']+)'", content)]
print(f"Found {len(broken_positions)} broken patterns")

fixes = []
for sep_pos, cid in broken_positions:
    obj_raw, obj_s, obj_e = extract_object(content, sep_pos + 1)
    if not obj_raw or f"id:'{cid}'" not in obj_raw:
        print(f"  {cid}: extract failed, skip"); continue
    fixes.append((sep_pos, obj_e, obj_raw, cid))

# 後ろから修正
fixes.sort(key=lambda x: x[0], reverse=True)
for sep_pos, obj_e, obj_raw, cid in fixes:
    new = "}\nwindow.CHAR_TEMPLATES.female.push(" + obj_raw + ");"
    content = content[:sep_pos] + new + content[obj_e:]
    print(f"  Fixed {cid}")

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f"Version: {old_ver} -> {new_ver}")

backup = r'C:\AI\ComfyUI\dashboard_backup_fixall_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html'
shutil.copy2(path, backup)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")

# 再スキャン
remaining = list(re.finditer(r"\},\n\{\n  id:'char_kakuseizai_", content))
print(f"Remaining broken: {len(remaining)}")
