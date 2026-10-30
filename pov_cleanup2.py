# -*- coding: utf-8 -*-
# 死にコードGD {key:'deliheru',...char_pov_deliheru_...} を削除
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
DB = r'C:\AI\ComfyUI\dashboard.html'
s = open(DB, encoding='utf-8').read()
pat = re.compile(r"\{key:'deliheru',label:\"[^\"]*\",fn:id => /\^char_pov_deliheru_/\.test\(id\)(?:,bigGenre:'[^']*')?\},\n*")
s, n = pat.subn('', s)
print('removed:', n)
assert n == 1, n
open(DB, 'w', encoding='utf-8', newline='').write(s)
# 残存はHTML仕様書表(<code>)内のみか確認
rest = [m.start() for m in re.finditer(r'char_pov_', s)]
bad = [i for i in rest if '<code>' not in s[max(0,i-60):i]]
print('remaining:', len(rest), 'non-doc:', len(bad))
assert len(bad) == 0, bad
print('OK')
