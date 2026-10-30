"""
kiroku_B〜最後のkirokuまでを配列形式に戻す
- '  });\nwindow.CHAR_TEMPLATES.female.push({' → '  },\n\n  {' (配列内の区切り)
- 最後のkirokuの '});' の後に ']); ' を追加して配列を閉じる
"""
import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# kiroku系のpushパターンを配列形式に変換
# '  });\nwindow.CHAR_TEMPLATES.female.push({\n\n    id:\'char_kiroku_' を
# '  },\n\n  {\n\n    id:\'char_kiroku_' に置換
old_pat = '  });\nwindow.CHAR_TEMPLATES.female.push({\n\n    id:\'char_kiroku_'
new_pat = '  },\n\n  {\n\n    id:\'char_kiroku_'
count = content.count(old_pat)
print(f"kiroku push pattern count: {count}")
content = content.replace(old_pat, new_pat)

# 最後のkirokuの後 '  });' を '  }]);' に変換する必要があるか確認
# まず現在の状況を確認
idx = content.find('char_kiroku_E') if 'char_kiroku_E' in content else content.find('char_kiroku_D')
if idx > 0:
    end = content.find('});', idx)
    print(f"Last kiroku end: {repr(content[end-5:end+30])}")
    # 次がkirokuでないならここで配列を閉じる
    after = content[end+3:end+100].strip()
    print(f"After last kiroku close: {repr(after[:80])}")
    if not after.startswith('{') and not 'char_kiroku' in after:
        content = content[:end] + '}]);' + content[end+3:]
        print("  Added ] to close array")

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)
shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_ka_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
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
