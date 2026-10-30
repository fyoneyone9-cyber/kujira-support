"""
S1 tifa/aerith/peach/mitsuri の outfits を jk_A の29シーンに置き換え
（キャラ固有の prompt/neg はそのまま維持）
"""
import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

def extract_outfits(content, char_id):
    """char_idのpushブロックからoutfitsの値（文字列）を抜き出す"""
    idx = content.find(char_id)
    if idx < 0: return None
    # outfits: の位置を探す
    ofs = content.find('outfits:', idx)
    if ofs < 0: return None
    # outfitsの値（[...]）を取得
    bracket_start = content.find('[', ofs)
    # 対応する ] を探す（ネスト考慮）
    depth = 0; i = bracket_start; in_str = False; sc = None
    while i < len(content):
        c = content[i]
        if in_str:
            if c == '\\': i += 2; continue
            if c == sc: in_str = False
        else:
            if c in ('"', "'"): in_str = True; sc = c
            elif c == '[': depth += 1
            elif c == ']':
                depth -= 1
                if depth == 0:
                    return content[bracket_start:i+1]
        i += 1
    return None

def replace_outfits(content, char_id, new_outfits_str):
    """char_idのoutfits値を new_outfits_str に置き換える"""
    idx = content.find(char_id)
    if idx < 0: return content, False
    ofs = content.find('outfits:', idx)
    if ofs < 0: return content, False
    bracket_start = content.find('[', ofs)
    depth = 0; i = bracket_start; in_str = False; sc = None
    while i < len(content):
        c = content[i]
        if in_str:
            if c == '\\': i += 2; continue
            if c == sc: in_str = False
        else:
            if c in ('"', "'"): in_str = True; sc = c
            elif c == '[': depth += 1
            elif c == ']':
                depth -= 1
                if depth == 0:
                    new = content[:bracket_start] + new_outfits_str + content[i+1:]
                    return new, True
        i += 1
    return content, False

# jk_A の outfits を取得
jka_outfits = extract_outfits(content, 'char_kakuseizai_jk_A')
if not jka_outfits:
    print("ERROR: jk_A outfits not found"); sys.exit(1)
print(f"jk_A outfits: {len(jka_outfits)} chars, scene count: {jka_outfits.count('label:')}")

# 4キャラに適用
for char_id in ['char_kakuseizai_tifa', 'char_kakuseizai_aerith', 'char_kakuseizai_peach', 'char_kakuseizai_mitsuri']:
    content, ok = replace_outfits(content, char_id, jka_outfits)
    print(f"  {char_id}: {'OK' if ok else 'NOT FOUND'}")

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)

shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_s1ofs_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")

scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
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
for i, err in errors[:3]:
    print("  block", i, ":", err[:150])
