import sys, re, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# より広いパターン: }, + 任意の空白改行 + { + \n  id:'char_
broken = [(m.start(), m.group(1)) for m in re.finditer(r"\}\s*,\s*\n\s*\{\n\s+id:'(char_[^']+)'", content)]
print("Found:", len(broken))

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

fixes = []
for sep_pos, cid in broken:
    # sepの } を見つける
    close_brace = content.rfind('}', 0, sep_pos + 1)
    obj_raw, _, obj_e = extract_object(content, close_brace + 1)
    if obj_raw and cid in obj_raw:
        fixes.append((close_brace, obj_e, obj_raw, cid))
    else:
        print("  SKIP:", cid)

fixes.sort(key=lambda x: x[0], reverse=True)
for close_brace, obj_e, obj_raw, cid in fixes:
    # close_braceの} + それ以降obj_eまでを "\nwindow...push(...);" に
    content = content[:close_brace+1] + "\nwindow.CHAR_TEMPLATES.female.push(" + obj_raw + ");" + content[obj_e:]
    print("  Fixed:", cid)

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)

shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_broad_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

# 残確認
remaining = list(re.finditer(r"\}\s*,\s*\n\s*\{\n\s+id:'char_", content))
print("Remaining:", len(remaining), "-> Done.")
