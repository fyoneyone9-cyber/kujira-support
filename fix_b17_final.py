"""
block17内の全 }); を }, に変換（配列形式に戻す）
その後のnode --checkで検証
"""
import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

sc17 = scripts_iter[17]
inner17 = sc17.group(1)

# step1: '  });' → '  },' (インデント付き)
count1 = inner17.count('  });')
inner17 = inner17.replace('  });', '  },')
# step2: '});' (インデントなし) → '},'
count2 = inner17.count('\n});')
inner17 = inner17.replace('\n});', '\n},')
print("Converted:  }); x", count1, "newline}); x", count2)

# step3: 孤立した ); (push の残り) → 削除
# '\n  {' が push で変換されたものなら既にOK
# step4: CHAR_TEMPLATES の配列が閉じているか最後を確認
# 最後は ]; で閉じるべき - 後で確認

content = content[:sc17.start(1)] + inner17 + content[sc17.end(1):]

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_b17f_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
    r = subprocess.run(['node', '--check', tmp.name], capture_output=True, timeout=20)
    os.unlink(tmp.name)
    err = r.stderr.decode('utf-8', errors='replace') if r.stderr else ''
    if r.returncode != 0:
        errors.append((i, err))
print("JS errors:", len(errors))
for i, err in errors[:5]:
    print("  block", i, ":", err[:200])
