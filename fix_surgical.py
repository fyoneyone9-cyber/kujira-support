import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

fixes_applied = 0

# ===== Fix 1: Block22 - rohypnol_youchien_B の裸の { を push({ に =====
# });(\n){\n  id:'char_rohypnol_youchien_B' のパターン
old = "});\n\n{\n  id:'char_rohypnol_youchien_B'"
new = "});\nwindow.CHAR_TEMPLATES.female.push({\n  id:'char_rohypnol_youchien_B'"
if old in content:
    content = content.replace(old, new, 1)
    print("Fix1 applied: rohypnol_youchien_B bare {")
    fixes_applied += 1
else:
    # 改行パターンが違う可能性
    m = re.search(r'\}\);\s*\n\s*\{\s*\n\s+id:\'char_rohypnol_youchien_B\'', content)
    if m:
        content = content[:m.start()] + '});\nwindow.CHAR_TEMPLATES.female.push({\n  id:\'char_rohypnol_youchien_B\'' + content[m.end():]
        print("Fix1 applied via regex: rohypnol_youchien_B")
        fixes_applied += 1
    else:
        print("Fix1 NOT FOUND")

# ===== Fix 2: Block24 - if(registerGenre){ の後の }); =====
# "if (window.registerGenre) {\n});\nwindow.CHAR_TEMPLATES.female.push({" パターン
# → "if (window.registerGenre) {\n}\nwindow.CHAR_TEMPLATES.female.push({"
m = re.search(r'(if \(window\.registerGenre\) \{[^}]*?)\};\)', content, re.DOTALL)
if not m:
    m = re.search(r'(if \(window\.registerGenre\) \{)\s*\n\}\);\nwindow', content)
if m:
    # }); → }\n のみ
    old2 = m.group(0)
    new2 = old2.replace('});\nwindow', '}\nwindow').replace(');\n}', '\n}')
    content = content.replace(old2, new2, 1)
    print("Fix2 applied: registerGenre if block")
    fixes_applied += 1
else:
    # より単純なパターン
    old2 = 'if (window.registerGenre) {\n});\nwindow.CHAR_TEMPLATES.female.push({'
    new2 = 'if (window.registerGenre) {\n}\nwindow.CHAR_TEMPLATES.female.push({'
    if old2 in content:
        content = content.replace(old2, new2, 1)
        print("Fix2 applied simple: registerGenre")
        fixes_applied += 1
    else:
        # スキャン
        idx = content.find("if (window.registerGenre)")
        while idx >= 0:
            seg = content[idx:idx+100]
            print("  registerGenre context:", repr(seg[:80]))
            idx = content.find("if (window.registerGenre)", idx+1)
            if idx > 50000000: break

# ===== Fix 3: Block17 - 余分な }); を削除 =====
# kiroku_A の push が二重になっている場合: });  + push({ で kirokuB
# 確認: `});\nwindow.CHAR_TEMPLATES.female.push({\n\n    id:'char_kiroku_B'`
# これは正常。エラーの原因は別の箇所か
# block17のkirkuAのoufits後が });  になっているが push( が前にない
idx_kB = content.find("id:'char_kiroku_B'")
if idx_kB > 0:
    before = content[idx_kB-200:idx_kB]
    print("kiroku_B before:", repr(before[-100:]))

# node --check で残りエラー確認
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
if fixes_applied > 0:
    ver_m = re.search(r'content="(\d{10,})"', content)
    if ver_m:
        old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
        content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
        print("Version:", old_ver, "->", new_ver)
    shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_surgical_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Saved.")

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
