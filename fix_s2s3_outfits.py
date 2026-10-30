import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

def extract_outfits(content, char_id):
    idx = content.find(char_id)
    if idx < 0: return None
    ofs = content.find('outfits:', idx)
    if ofs < 0: return None
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
                    return content[bracket_start:i+1]
        i += 1
    return None

def replace_outfits(content, char_id, new_outfits_str):
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
                    return content[:bracket_start] + new_outfits_str + content[i+1:], True
        i += 1
    return content, False

# S2: char_kakuseizai_s2_jk_A の outfits を donor に
s2_donor = extract_outfits(content, 'char_kakuseizai_s2_jk_A')
print(f"S2 donor outfits: {len(s2_donor) if s2_donor else 'NOT FOUND'} chars")
if s2_donor:
    for char_id in ['char_kakuseizai_s2_peach', 'char_kakuseizai_s2_mitsuri']:
        content, ok = replace_outfits(content, char_id, s2_donor)
        print(f"  {char_id}: {'OK' if ok else 'NOT FOUND'}")

# S3: char_kakuseizai_s3_jk_A の outfits を donor に
s3_donor = extract_outfits(content, 'char_kakuseizai_s3_jk_A')
print(f"S3 donor outfits: {len(s3_donor) if s3_donor else 'NOT FOUND'} chars")
if s3_donor:
    for char_id in ['char_kakuseizai_s3_ff_tifa', 'char_kakuseizai_s3_ff_aerith', 'char_kakuseizai_s3_peach', 'char_kakuseizai_s3_mitsuri']:
        content, ok = replace_outfits(content, char_id, s3_donor)
        print(f"  {char_id}: {'OK' if ok else 'NOT FOUND'}")

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)

shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_s23ofs_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
