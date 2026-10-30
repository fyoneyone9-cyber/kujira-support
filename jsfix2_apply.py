# -*- coding: utf-8 -*-
# Fix: GD削除で残った孤立トークンを除去し、node --checkで両ブロックの構文回復を確認してから保存
# block5: html 3088(' },') 3090(' }') 3092(',') / block21: html 24425('    },')
import re, sys, io, os, shutil, time, subprocess, tempfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
DB = r'C:\AI\ComfyUI\dashboard.html'
ts = time.strftime('%Y%m%d_%H%M%S')
bak = DB.replace('.html', f'_backup_{ts}_jsfix2.html')
shutil.copy2(DB, bak)
print('backup:', bak)

src = open(DB, encoding='utf-8').read()
lines = src.split('\n')

# 対象行の内容を確認してから削除（1-index: 3088, 3090, 3092, 24425）
targets = {3088: ' },', 3090: ' }', 3092: ',', 24425: '    },'}
for ln, expect in targets.items():
    actual = lines[ln-1]
    assert actual == expect, (ln, repr(actual))
# 後ろから削除（index ずれ防止）
for ln in sorted(targets, reverse=True):
    del lines[ln-1]
fixed = '\n'.join(lines)

# 全scriptブロック再検証
tmpdir = tempfile.mkdtemp()
bad = []
blocks = list(re.finditer(r'<script(?:\s[^>]*)?>(.*?)</script>', fixed, re.DOTALL))
for idx, m in enumerate(blocks):
    body = m.group(1)
    if len(body.strip()) < 10:
        continue
    p = os.path.join(tmpdir, f'b{idx}.js')
    open(p, 'w', encoding='utf-8').write(body)
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
    if r.returncode != 0:
        bad.append((idx, fixed[:m.start()].count('\n')+1, r.stderr[:300]))
print('bad blocks after fix:', len(bad))
for b in bad:
    print(b)
assert len(bad) == 0, 'still broken'

open(DB, 'w', encoding='utf-8', newline='').write(fixed)
print('saved. ALL SCRIPT BLOCKS SYNTAX OK')
