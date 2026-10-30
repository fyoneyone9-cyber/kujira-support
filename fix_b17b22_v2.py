import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

# Block17: outfits行(65058)の末尾を確認して、outfitsが閉じているかチェック
sc17 = scripts_iter[17]
lines17 = sc17.group(1).split('\n')
outfits_line = lines17[65057]  # 65058行 (0-indexed: 65057)
# outfitsの [ が閉じているか
d = 0
for c in outfits_line:
    if c == '[': d += 1
    elif c == ']': d -= 1
print(f"Block17 outfits line bracket balance: {d}")
# d==0なら閉じている → 65060の }); は正常（outfitsの後のpushブロック閉じ）
# d!=0なら 65060の }); が先にあってoutfitsが閉じていない
# → 65060行を ']};' ではなく確認
print("Block17 65060:", repr(lines17[65059]))

# Block22: 155行 (index 154) が } → });
sc22 = scripts_iter[22]
lines22 = sc22.group(1).split('\n')
print("Block22 155:", repr(lines22[154]))
if lines22[154].strip() == '}':
    lines22[154] = '});'
    print("  Fixed: } -> });")
new22 = '\n'.join(lines22)
content = content[:sc22.start(1)] + new22 + content[sc22.end(1):]

# Block17の65060が }); で正しいが outfitsが閉じていない場合
# outfits行の末尾に ] を補完
scripts_iter2 = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17b = scripts_iter2[17]
lines17b = sc17b.group(1).split('\n')
outfits_line2 = lines17b[65057]
d2 = 0
for c in outfits_line2:
    if c == '[': d2 += 1
    elif c == ']': d2 -= 1
print(f"Block17 outfits bracket balance after: {d2}")
if d2 > 0:
    # outfits行の末尾に閉じ括弧を追加
    lines17b[65057] = lines17b[65057] + ']' * d2
    print(f"  Added {d2} closing ] to outfits line")
    new17 = '\n'.join(lines17b)
    content = content[:sc17b.start(1)] + new17 + content[sc17b.end(1):]

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_b17b22_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
