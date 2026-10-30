# -*- coding: utf-8 -*-
# 大ジャンル「学年・職業」「アニメ・芸能」「アニメ・芸能・コラボ」配下の全グループとIDパターンを調査
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
targets = ['学年・職業', 'アニメ・芸能', 'アニメ・芸能・コラボ']
# bigGenre付きfn形式GD
found = {}
for m in re.finditer(r"\{key:'([^']+)',label:\"([^\"]*)\",fn:id => ([^\n]*?),bigGenre:'([^']*)'\},", s):
    bg = m.group(4)
    if any(t in bg for t in targets):
        found.setdefault(bg, []).append((m.group(1), m.group(2), m.group(3)[:90]))
for bg, rows in found.items():
    print('===', bg, len(rows))
    for k, l, f in rows:
        print(' ', k, '|', l, '|', f)
