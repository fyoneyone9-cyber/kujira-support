"""
S3 peach/mitsuri の構文エラー修正
,\n{id:...}\n形式 → window.CHAR_TEMPLATES.female.push({...}); 形式に変換
"""
import sys, re, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# 問題箇所: if (window.registerGenre) {\n},\n{\n  id:'char_kakuseizai_s3_peach'...
# を以下に修正:
# if (window.registerGenre) {\n}\n
# window.CHAR_TEMPLATES.female.push({...});\n
# window.CHAR_TEMPLATES.female.push({...});\n

# まず壊れたブロックを特定
# "},\n{\n  id:'char_kakuseizai_s3_peach'" を検索
BROKEN_SEP = "},\n{\n  id:'char_kakuseizai_s3_peach'"
idx = content.find(BROKEN_SEP)
print(f"Broken separator at: {idx}")
if idx < 0:
    # 別パターンも試す
    BROKEN_SEP = "},\n{\n  id:'char_kakuseizai_s3_peach'"
    idx = content.find(BROKEN_SEP)
    print(f"Alt pattern at: {idx}")

if idx < 0:
    print("Cannot find broken pattern, checking context around s3_peach...")
    s3p = content.find("id:'char_kakuseizai_s3_peach'")
    print(f"s3_peach at: {s3p}")
    print(f"Before: {content[s3p-30:s3p]!r}")
    sys.exit(1)

# S3 peach/mitsuri の2ブロックを抽出してpush形式に変換
# "},\n{...s3_peach...},\n{...s3_mitsuri...}\n" の範囲を特定

# idx は "}" の位置
# その後ろの2ブロックを取得
def extract_object(content, start):
    """{ ... } のオブジェクトを抽出"""
    s = content.find('{', start)
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

# "}" の直後から2つのオブジェクトを取得
obj1_raw, obj1_s, obj1_e = extract_object(content, idx + 1)
obj2_raw, obj2_s, obj2_e = extract_object(content, obj1_e)
print(f"obj1: {obj1_s}-{obj1_e}, id: {'char_kakuseizai_s3_peach' in obj1_raw}")
print(f"obj2: {obj2_s}-{obj2_e}, id: {'char_kakuseizai_s3_mitsuri' in obj2_raw}")

# 全体の置換範囲: idx("}") から obj2_e まで
# "},\n{...peach...},\n{...mitsuri...}" → "}\nwindow.CHAR_TEMPLATES.female.push({...peach...});\nwindow.CHAR_TEMPLATES.female.push({...mitsuri...});"

old_str = content[idx:obj2_e]
new_str = "}\nwindow.CHAR_TEMPLATES.female.push(" + obj1_raw + ");\nwindow.CHAR_TEMPLATES.female.push(" + obj2_raw + ");"

print(f"\nReplacing {len(old_str)} chars with {len(new_str)} chars")
print(f"Old start: {old_str[:50]!r}")
print(f"New start: {new_str[:50]!r}")

new_content = content[:idx] + new_str + content[obj2_e:]

# バージョン更新
ver_m = re.search(r'content="(\d{10,})"', new_content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    new_content = new_content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f"Version: {old_ver} -> {new_ver}")

backup = r'C:\AI\ComfyUI\dashboard_backup_s3fix_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html'
shutil.copy2(path, backup)
with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Saved.")

# 検証
for cid in ['char_kakuseizai_s3_peach', 'char_kakuseizai_s3_mitsuri']:
    ok = f"female.push({{" in new_content[new_content.find(f"id:'{cid}'") - 40: new_content.find(f"id:'{cid}'")]
    print(f"  {cid} push形式: {'OK' if ok else 'NG'}")
