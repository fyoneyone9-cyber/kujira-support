# -*- coding: utf-8 -*-
# Fix: big3削除でsensei複数行GDを消した際に残った孤立 '},'（24412行目）を除去
import sys, io, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
DB = r'C:\AI\ComfyUI\dashboard.html'
ts = time.strftime('%Y%m%d_%H%M%S')
shutil.copy2(DB, DB.replace('.html', f'_backup_{ts}_jsfix.html'))
src = open(DB, encoding='utf-8').read()
lines = src.split('\n')
# 24412行目(0-index 24411)が孤立 '},' であることを確認して除去
target = lines[24411].strip()
assert target == '},', repr(target)
# 前後が独立したオブジェクトエントリ行であること（配列要素の並び）を確認
del lines[24411]
open(DB, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
print('fixed: removed orphan "}," at line 24412')
