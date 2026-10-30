# -*- coding: utf-8 -*-
# ロリ妖精S1-10 + ロリサキュバスS1-10 + 小児科医S1-10 削除
# （計180体 + GD30 + outfit sets S0512-S0521, S0532-S0541, S0592-S0601）
import re, sys, io, json, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ts = time.strftime('%Y%m%d_%H%M%S')
DB = r'C:\AI\ComfyUI\dashboard.html'
OS_JSON = r'C:\AI\ComfyUI\outfit_sets.json'

db_bak = DB.replace('.html', f'_backup_{ts}_del3b.html')
os_bak = OS_JSON.replace('.json', f'_backup_{ts}_del3b.json')
shutil.copy2(DB, db_bak); shutil.copy2(OS_JSON, os_bak)
print('backup:', db_bak)
print('backup:', os_bak)

s = open(DB, encoding='utf-8').read()

push_pat = re.compile(r"CHAR_TEMPLATES\.female\.push\(\{id:'char_(?:lolifairy|lolisucc|shouni)_s\d+_[^']*'.*?\}\);\n")
s, n_push = push_pat.subn('', s)
print('push removed:', n_push)
assert n_push == 180, n_push

gd_pat = re.compile(r"\{key:'(?:lolifairy|lolisucc|shouni)_s\d+',label:\"[^\"]*\",fn:id => /\^char_(?:lolifairy|lolisucc|shouni)_s\d+_/\.test\(id\)(?:,bigGenre:'[^']*')?\},")
s, n_gd = gd_pat.subn('', s)
print('groupdef removed:', n_gd)
assert n_gd == 30, n_gd

rest = (s.count('char_lolifairy_s') + s.count('char_lolisucc_s') + s.count('char_shouni_s')
        + len(re.findall(r"'(?:lolifairy|lolisucc|shouni)_s\d+'", s)))
print('remaining refs:', rest)
assert rest == 0

# 他のサキュバス系（succubus/suc_iny/suc_solo/kaizou2_succubus/succubus_duo）が無傷か確認
for keep in ['char_succubus_', 'char_suc_iny_', 'char_suc_solo_']:
    print('keep check', keep, s.count(keep) > 0)

m = re.search(r'name="version" content="(\d+)"', s)
old = m.group(1); new = str(int(old)+1)
s = s.replace(f'content="{old}"', f'content="{new}"', 1)
print('version:', old, '->', new)
open(DB, 'w', encoding='utf-8', newline='').write(s)

d = json.load(open(OS_JSON, encoding='utf-8'))
keys = ['S0%d' % n for n in list(range(512, 522)) + list(range(532, 542)) + list(range(592, 602))]
removed = [k for k in keys if d.pop(k, None) is not None]
print('outfit sets removed:', len(removed), removed)
assert len(removed) == 30, removed
json.dump(d, open(OS_JSON, 'w', encoding='utf-8'), ensure_ascii=False)
print('outfit_sets keys:', len(d))

s2 = open(DB, encoding='utf-8').read()
d2 = json.load(open(OS_JSON, encoding='utf-8'))
assert 'char_lolifairy_s' not in s2 and 'char_lolisucc_s' not in s2 and 'char_shouni_s' not in s2
assert all(k not in d2 for k in keys)
print('VERIFY OK')
