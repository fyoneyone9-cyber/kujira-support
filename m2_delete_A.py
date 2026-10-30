# -*- coding: utf-8 -*-
# ロリ人形S1-10 + 愛玩児飼育S1-10 削除（計120体 + GD20 + outfit sets 20）
import re, sys, io, json, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ts = time.strftime('%Y%m%d_%H%M%S')
DB = r'C:\AI\ComfyUI\dashboard.html'
OS_JSON = r'C:\AI\ComfyUI\outfit_sets.json'

db_bak = DB.replace('.html', f'_backup_{ts}_m2del.html')
os_bak = OS_JSON.replace('.json', f'_backup_{ts}_m2del.json')
shutil.copy2(DB, db_bak); shutil.copy2(OS_JSON, os_bak)
print('backup:', db_bak)
print('backup:', os_bak)

s = open(DB, encoding='utf-8').read()

push_pat = re.compile(r"CHAR_TEMPLATES\.female\.push\(\{id:'char_(?:lolidoll|aigan)_s\d+_[^']*'.*?\}\);\n")
s, n_push = push_pat.subn('', s)
print('push removed:', n_push)
assert n_push == 120, n_push

gd_pat = re.compile(r"\{key:'(?:lolidoll|aigan)_s\d+',label:\"[^\"]*\",fn:id => /\^char_(?:lolidoll|aigan)_s\d+_/\.test\(id\)\},")
s, n_gd = gd_pat.subn('', s)
print('groupdef removed:', n_gd)
assert n_gd == 20, n_gd

rest = s.count('char_lolidoll_s') + s.count('char_aigan_s') + len(re.findall(r"'(?:lolidoll|aigan)_s\d+'", s))
print('remaining refs:', rest)
assert rest == 0

m = re.search(r'name="version" content="(\d+)"', s)
old = m.group(1); new = str(int(old)+1)
s = s.replace(f'content="{old}"', f'content="{new}"', 1)
print('version:', old, '->', new)
open(DB, 'w', encoding='utf-8', newline='').write(s)

d = json.load(open(OS_JSON, encoding='utf-8'))
keys = ['S0%d' % n for n in list(range(462,472)) + list(range(612,622))]
removed = [k for k in keys if d.pop(k, None) is not None]
print('outfit sets removed:', removed)
assert len(removed) == 20, removed
json.dump(d, open(OS_JSON, 'w', encoding='utf-8'), ensure_ascii=False)
print('outfit_sets keys:', len(d))

s2 = open(DB, encoding='utf-8').read()
d2 = json.load(open(OS_JSON, encoding='utf-8'))
assert 'char_lolidoll_s' not in s2 and 'char_aigan_s' not in s2
assert all(k not in d2 for k in keys)
print('VERIFY OK')
