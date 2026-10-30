"""
S1/S2/S3 peach/mitsuri 全6キャラの構文エラー一括修正
},\n{id:... → window.CHAR_TEMPLATES.female.push({...});
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

TARGETS = [
    'char_kakuseizai_peach',
    'char_kakuseizai_mitsuri',
    'char_kakuseizai_s2_peach',
    'char_kakuseizai_s2_mitsuri',
    # s3は既に修正済みだが念のため確認
    'char_kakuseizai_s3_peach',
    'char_kakuseizai_s3_mitsuri',
]

# 後ろから処理して位置ずれを防ぐ
fixes = []
for cid in TARGETS:
    idx = content.find(f"id:'{cid}'")
    if idx < 0:
        print(f"{cid}: NOT FOUND")
        continue
    before = content[idx-4:idx]
    if before != "  id":  # already push形式の可能性
        print(f"{cid}: unexpected before={before!r}, skip")
        continue
    # "},\n{" の位置を探す（このブロックの直前）
    sep_pos = content.rfind('},\n{', 0, idx)
    if sep_pos < 0:
        print(f"{cid}: no broken sep found")
        continue
    # sep_pos: "}" の位置
    obj_raw, obj_s, obj_e = extract_object(content, sep_pos + 1)
    if not obj_raw or f"id:'{cid}'" not in obj_raw:
        print(f"{cid}: object extraction failed or wrong object")
        continue
    print(f"{cid}: sep={sep_pos} obj={obj_s}-{obj_e} ({len(obj_raw)}chars)")
    fixes.append((sep_pos, obj_e, obj_raw))

# 後ろから置換
fixes.sort(key=lambda x: x[0], reverse=True)
for sep_pos, obj_e, obj_raw in fixes:
    old = content[sep_pos:obj_e]
    new = "}\nwindow.CHAR_TEMPLATES.female.push(" + obj_raw + ");"
    content = content[:sep_pos] + new + content[obj_e:]
    print(f"  Fixed: {old[:40]!r} -> push()")

# バージョン更新
ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f"Version: {old_ver} -> {new_ver}")

backup = r'C:\AI\ComfyUI\dashboard_backup_allfix_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html'
shutil.copy2(path, backup)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")

# 最終確認
for cid in TARGETS:
    idx = content.find(f"id:'{cid}'")
    before = content[idx-50:idx]
    is_push = 'female.push({' in before or "female.push({\n  id" in before or "female.push({id" in before
    # push({\n  id:... の形
    is_push2 = 'female.push(' in content[idx-60:idx]
    print(f"  {cid}: {'OK(push)' if is_push2 else 'NG: ' + repr(before[-30:])}")
