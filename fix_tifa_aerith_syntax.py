"""
tifa/aerith S1ブロックの構文修正
},\n{id:'char_kakuseizai_tifa' → window.CHAR_TEMPLATES.female.push({...});
},\n{id:'char_kakuseizai_aerith' → window.CHAR_TEMPLATES.female.push({...});
"""
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

TARGETS = ['char_kakuseizai_tifa', 'char_kakuseizai_aerith']

fixes = []
for cid in TARGETS:
    idx = content.find(f"id:'{cid}'")
    if idx < 0:
        print(f"{cid}: NOT FOUND"); continue
    before = content[idx-30:idx]
    if 'female.push(' in before:
        print(f"{cid}: already push form, skip"); continue
    sep_pos = content.rfind('},\n{', 0, idx)
    if sep_pos < 0:
        print(f"{cid}: no broken sep"); continue
    obj_raw, obj_s, obj_e = extract_object(content, sep_pos + 1)
    if not obj_raw or f"id:'{cid}'" not in obj_raw:
        print(f"{cid}: wrong object"); continue
    print(f"{cid}: sep={sep_pos} len={len(obj_raw)}")
    fixes.append((sep_pos, obj_e, obj_raw))

fixes.sort(key=lambda x: x[0], reverse=True)
for sep_pos, obj_e, obj_raw in fixes:
    new = "}\nwindow.CHAR_TEMPLATES.female.push(" + obj_raw + ");"
    content = content[:sep_pos] + new + content[obj_e:]
    print(f"  Fixed {sep_pos}")

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f"Version: {old_ver} -> {new_ver}")

backup = r'C:\AI\ComfyUI\dashboard_backup_tifafix_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html'
shutil.copy2(path, backup)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")

for cid in TARGETS:
    idx = content.find(f"id:'{cid}'")
    ok = 'female.push(' in content[idx-60:idx]
    print(f"  {cid}: {'OK' if ok else 'NG'}")
