"""
block17 の const CHAR_TEMPLATES = { female: [...] } 配列形式を
全て window.CHAR_TEMPLATES.female.push({...}); 形式に統一する。

手順:
1. block17の CHAR_TEMPLATES 定義 = { female: [] }; に変更
2. 元配列から各キャラオブジェクトを抽出
3. push() 形式で追記
"""
import re, sys, shutil, datetime, subprocess, tempfile, os, json
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'

# バックアップ
ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
backup = r'C:\AI\ComfyUI\dashboard_backup_unify_' + ts + '.html'
shutil.copy2(path, backup)
print("Backup:", backup)

with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts_iter[17]
inner17 = sc17.group(1)

# CHAR_TEMPLATES 定義の開始位置を探す
ct_match = re.search(r'const CHAR_TEMPLATES\s*=\s*\{', inner17)
if not ct_match:
    print("ERROR: CHAR_TEMPLATES not found")
    sys.exit(1)
ct_start = ct_match.start()
print(f"CHAR_TEMPLATES at block17 offset {ct_start}")

# female: [ の開始位置
female_match = re.search(r'female\s*:\s*\[', inner17[ct_start:])
female_start = ct_start + female_match.end()  # '[' の次の位置
print(f"female array starts at offset {female_start}")

# female配列の終わり（対応する ] を探す）
depth = 1; i = female_start; in_str = False; sc_c = None
while i < len(inner17) and depth > 0:
    c = inner17[i]
    if in_str:
        if c == '\\': i += 2; continue
        if c == sc_c: in_str = False
    else:
        if c in ('"', "'"): in_str = True; sc_c = c
        elif c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                female_end = i  # ']' の位置
                break
    i += 1
print(f"female array ends at offset {female_end}")

array_content = inner17[female_start:female_end]
print(f"Array content length: {len(array_content)} chars")

# 配列内の各キャラオブジェクトを抽出（深度1の { ... } ブロック）
chars = []
pos = 0
while pos < len(array_content):
    # 次の { を探す
    brace_start = array_content.find('{', pos)
    if brace_start < 0:
        break
    # 対応する } を探す
    depth2 = 0; j = brace_start; in_str2 = False; sc_c2 = None
    while j < len(array_content):
        c = array_content[j]
        if in_str2:
            if c == '\\': j += 2; continue
            if c == sc_c2: in_str2 = False
        else:
            if c in ('"', "'"): in_str2 = True; sc_c2 = c
            elif c == '{': depth2 += 1
            elif c == '}':
                depth2 -= 1
                if depth2 == 0:
                    chars.append(array_content[brace_start:j+1])
                    pos = j + 1
                    break
        j += 1
    else:
        break

print(f"Extracted {len(chars)} char objects from female array")

# 各キャラのidを確認
for i, ch in enumerate(chars[:3]):
    id_m = re.search(r"id\s*:\s*['\"]([^'\"]+)['\"]", ch)
    print(f"  [{i}] id={id_m.group(1) if id_m else '?'}")
print("  ...")
for i, ch in enumerate(chars[-3:]):
    id_m = re.search(r"id\s*:\s*['\"]([^'\"]+)['\"]", ch)
    print(f"  [{len(chars)-3+i}] id={id_m.group(1) if id_m else '?'}")

# block17の CHAR_TEMPLATES 定義ブロック全体を特定
# (外側の {} も含む: const CHAR_TEMPLATES = { ... };)
ct_outer_start = ct_start
# 対応する } を探す
depth3 = 0; k = ct_start; in_str3 = False; sc_c3 = None
found_open = False
while k < len(inner17):
    c = inner17[k]
    if in_str3:
        if c == '\\': k += 2; continue
        if c == sc_c3: in_str3 = False
    else:
        if c in ('"', "'"): in_str3 = True; sc_c3 = c
        elif c == '{':
            depth3 += 1
            found_open = True
        elif c == '}':
            depth3 -= 1
            if found_open and depth3 == 0:
                ct_outer_end = k + 1
                # セミコロンも含む
                m = re.match(r'\s*;', inner17[ct_outer_end:])
                if m: ct_outer_end += m.end()
                break
    k += 1
print(f"CHAR_TEMPLATES block: offset {ct_outer_start} - {ct_outer_end}")
print(f"Block length: {ct_outer_end - ct_outer_start}")

# 置換内容を作成
push_lines = ['window.CHAR_TEMPLATES = window.CHAR_TEMPLATES || { female: [], male: [] };\n']
for ch in chars:
    # オブジェクト内の余分な改行を整理
    obj = ch.strip()
    push_lines.append(f'window.CHAR_TEMPLATES.female.push({obj});\n')

replacement = '\n' + ''.join(push_lines) + '\n'
print(f"Replacement length: {len(replacement)} chars")
print(f"Push count: {len(chars)}")

# block17を置換
new_inner17 = inner17[:ct_outer_start] + replacement + inner17[ct_outer_end:]
content = content[:sc17.start(1)] + new_inner17 + content[sc17.end(1):]

# バージョン更新
ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")

# JS検証
print("Running node --check on all script blocks...")
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
errors = []
for idx, sc in enumerate(scripts):
    sc2 = sc.strip()
    if not sc2 or len(sc2) < 20: continue
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
    tmp.write(sc2); tmp.close()
    r = subprocess.run(['node', '--check', tmp.name], capture_output=True, timeout=30)
    os.unlink(tmp.name)
    err = r.stderr.decode('utf-8', errors='replace') if r.stderr else ''
    if r.returncode != 0:
        errors.append((idx, err))
print(f"JS errors: {len(errors)}")
for idx, err in errors[:5]:
    print(f"  block {idx}: {err[:300]}")

if len(errors) == 0:
    print("SUCCESS: All JS blocks valid!")
