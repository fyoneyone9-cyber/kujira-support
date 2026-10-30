import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# パターン1: });\n + (空白/コメント行)* + {\n  id:'char_ → }\n + push({ に変換
# つまり "});" が push(の閉じとして機能しているが、次の { が push なしで孤立している
count = 0
while True:
    m = re.search(r'\}\);\s*\n(\s*//[^\n]*)?\s*\n\{\s*\n\s+id:\'char_', content, re.DOTALL)
    if not m: break
    # m.start()が });の位置
    # 閉じ}) をそのままにして、次の { をpush({に変換
    close_bracket_end = content.index(');', m.start()) + 2  # }); の終わり
    brace_start = content.index('{', close_bracket_end)  # 次の {
    old = content[close_bracket_end:brace_start+1]
    new = '\nwindow.CHAR_TEMPLATES.female.push({'
    content = content[:close_bracket_end] + new + content[brace_start+1:]
    count += 1

print("Pattern1 fixes:", count)

# パターン2: block17のような });\nwindow...push({\n が正常なのにエラーになる場合
# → kirokuAのoutfitsの後に }); があるが push( が kirokuAの前にある
# kirokuAの context確認
idx = content.find("id:'char_kiroku_A'")
if idx < 0: idx = content.find('id:\'char_kiroku_A\'')
if idx > 0:
    before100 = content[idx-200:idx]
    print("kiroku_A before:", repr(before100[-100:]))
    after100 = content[idx:idx+50]
    print("kiroku_A id line:", repr(after100))

# block17 65058行 = kirokuAのoutfitsの後 → });
# これは push( + {kirokuA outfits} + ); の形なのに });が空になっているはず
# → もしかしてkirkuAのoutfitsが truncated で } の閉じが先に来ている

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)

shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_ultimate_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")

# JS check
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
print("Remaining JS errors:", len(errors))
for i, err in errors[:5]:
    print("  block", i, ":", err[:200])
