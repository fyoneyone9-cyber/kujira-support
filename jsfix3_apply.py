# -*- coding: utf-8 -*-
# Fix: push( {...}, {...}, ← の閉じ ')' が削除時に消えて '  ;' だけ残った → '  );' に復元
# 修正後、全scriptブロックをnode --checkで再検証してから保存
import re, sys, io, os, shutil, time, subprocess, tempfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
DB = r'C:\AI\ComfyUI\dashboard.html'
ts = time.strftime('%Y%m%d_%H%M%S')
bak = DB.replace('.html', f'_backup_{ts}_jsfix3.html')
shutil.copy2(DB, bak)
print('backup:', bak)

src = open(DB, encoding='utf-8').read()
lines = src.split('\n')
idx = 415362 - 1
assert lines[idx].strip() == ';', repr(lines[idx])
lines[idx] = '  );'
fixed = '\n'.join(lines)

tmpdir = tempfile.mkdtemp()
bad = []
for i, m in enumerate(re.finditer(r'<script(?:\s[^>]*)?>(.*?)</script>', fixed, re.DOTALL)):
    body = m.group(1)
    if len(body.strip()) < 10:
        continue
    p = os.path.join(tmpdir, f'b{i}.js')
    open(p, 'w', encoding='utf-8').write(body)
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
    if r.returncode != 0:
        bad.append((i, fixed[:m.start()].count('\n')+1, r.stderr[:300]))
print('bad blocks after fix:', len(bad))
for b in bad:
    print(b)
assert len(bad) == 0

# version bump
m = re.search(r'name="version" content="(\d+)"', fixed)
old = m.group(1); new = str(int(old)+1)
fixed = fixed.replace('content="%s"' % old, 'content="%s"' % new, 1)
print('version:', old, '->', new)
open(DB, 'w', encoding='utf-8', newline='').write(fixed)
print('saved. ALL SCRIPT BLOCKS SYNTAX OK')
