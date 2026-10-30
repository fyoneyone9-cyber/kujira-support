import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

# Block22: });, を全部 }); に
sc22 = scripts_iter[22]
inner22 = sc22.group(1)
count = inner22.count('});,')
inner22 = inner22.replace('});,', '});')
print("Block22: fixed });, x", count)
content = content[:sc22.start(1)] + inner22 + content[sc22.end(1):]

# Block17: depth計算して65060手前の状況を把握
scripts_iter2 = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts_iter2[17]
inner17 = sc17.group(1)
lines17 = inner17.split('\n')
# 65059行まで（0-indexed: 65058）のchunkのdepth
chunk = '\n'.join(lines17[:65059])
depth = 0; in_str = False; sc_c = None; i = 0
while i < len(chunk):
    c = chunk[i]
    if in_str:
        if c == '\\': i += 2; continue
        if c == sc_c: in_str = False
    else:
        if c in ('"', "'"): in_str = True; sc_c = c
        elif c in ('(','[','{'): depth += 1
        elif c in (')',']','}'): depth -= 1
    i += 1
print(f"Block17 depth before line 65060: {depth}")
# depth=1 → push( が開いたまま → 65060の }); が正しい（push閉じ）
# depth=0 → push が既に閉じている → 65060の }); が余分

if depth == 0:
    # 65060の }); を削除
    if lines17[65059].strip() == '});':
        lines17[65059] = ''
        print("Block17: Removed orphan }); at 65060")
        new17 = '\n'.join(lines17)
        content = content[:sc17.start(1)] + new17 + content[sc17.end(1):]
elif depth == 1:
    print("Block17: }); at 65060 is correct (closes push), no change needed")
    # エラーの原因は別の場所 → 65058のoutfitsが問題かもしれない
    # outfits行がtrunucatedなら最後に ] を足す必要あり
    print("  outfits line end:", repr(lines17[65057][-30:]))

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_fc_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
for i, err in errors[:5]:
    print("  block", i, ":", err[:200])
