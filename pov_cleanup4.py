# -*- coding: utf-8 -*-
# デリヘルPOVサブグループ3件（deliheru_youjo/shougaku/chuugaku）を削除
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
DB = r'C:\AI\ComfyUI\dashboard.html'
s = open(DB, encoding='utf-8').read()
pat = re.compile(r"\{\s*key:'deliheru_(?:youjo|shougaku|chuugaku)',\s*label:'[^']*',\s*fn: function\(id\)\{ return /\^char_pov_deliheru_(?:youjo|shougaku|chuugaku)_/\.test\(id\); \} \},\n*")
s, n = pat.subn('', s)
print('removed:', n)
assert n == 3, n
open(DB, 'w', encoding='utf-8', newline='').write(s)
# 最終確認: id定義ゼロ・UIグループ参照ゼロ
rest = [m.start() for m in re.finditer(r'char_pov_', s)]
print('remaining char_pov_ occurrences:', len(rest))
print('OK')
