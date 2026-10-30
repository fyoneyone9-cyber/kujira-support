import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# block22の {id:'char_kakuseizai_s2_' で始まる1行オブジェクト（push なし）を修正
# "\n{id:'char_" → "\nwindow.CHAR_TEMPLATES.female.push({id:'char_..."
# 対象はblock22内のみ
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc22 = scripts_iter[22]
inner22 = sc22.group(1)

# {id:'char_ で始まる行（pushなし、単独行）を push({ に変換
# 末尾が } または )} なら }); に変換
lines22 = inner22.split('\n')
fixed = 0
for j in range(len(lines22)):
    l = lines22[j]
    if re.match(r'^\{id:\'char_', l.strip()) and 'push(' not in lines22[j]:
        # この行が1行オブジェクト: {id:'...',outfits:[...]}
        stripped = l.strip()
        if stripped.endswith('}'):
            lines22[j] = 'window.CHAR_TEMPLATES.female.push(' + stripped + ');'
            fixed += 1
        else:
            lines22[j] = 'window.CHAR_TEMPLATES.female.push(' + stripped
            # 次の行でオブジェクトが閉じているか確認
            # 複数行スパンの場合はそのままにしてfind_matching_braceで閉じる
            # とりあえず単純に1行オブジェクトとして扱う（他のケース不明）

print("Fixed 1-line bare objects:", fixed)
new22 = '\n'.join(lines22)
content = content[:sc22.start(1)] + new22 + content[sc22.end(1):]

# block17 65072行エラーを確認
scripts_iter2 = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts_iter2[17]
inner17 = sc17.group(1).split('\n')
# 65072-65076付近
print("Block17 65070-65078:")
for j in range(65069, 65079):
    if j < len(inner17): print(j+1, repr(inner17[j][:100]))

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_ol_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")

scripts_final = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
errors = []
for i, sc in enumerate(scripts_final):
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
