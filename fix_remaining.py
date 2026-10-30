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

broken = [(m.start(), m.group(1)) for m in re.finditer(r"\},\n\{\n  id:'(char_[^']+)'", content)]
print("Found:", len(broken))
fixes = []
for sep_pos, cid in broken:
    obj_raw, _, obj_e = extract_object(content, sep_pos + 1)
    if obj_raw and cid in obj_raw:
        fixes.append((sep_pos, obj_e, obj_raw, cid))

fixes.sort(key=lambda x: x[0], reverse=True)
for sep_pos, obj_e, obj_raw, cid in fixes:
    content = content[:sep_pos] + "}\nwindow.CHAR_TEMPLATES.female.push(" + obj_raw + ");" + content[obj_e:]
    print("  Fixed:", cid)

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)

shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_final_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

remaining = len(list(re.finditer(r"\},\n\{\n  id:'char_", content)))
print("Remaining:", remaining, "-> Saved.")
