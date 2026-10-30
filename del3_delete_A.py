# -*- coding: utf-8 -*-
# ロリ催眠アプリS1-10(60体) + 実父が売るS1-10(60体) + 女湯露天盗撮(9体・複数行push形式) 削除
# 注意: char_tousatsu_youchien_(盗撮園児)・温泉盗撮(char_onsen_)は対象外
import re, sys, io, json, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ts = time.strftime('%Y%m%d_%H%M%S')
DB = r'C:\AI\ComfyUI\dashboard.html'
OS_JSON = r'C:\AI\ComfyUI\outfit_sets.json'

db_bak = DB.replace('.html', f'_backup_{ts}_del3.html')
os_bak = OS_JSON.replace('.json', f'_backup_{ts}_del3.json')
shutil.copy2(DB, db_bak); shutil.copy2(OS_JSON, os_bak)
print('backup:', db_bak)
print('backup:', os_bak)

s = open(DB, encoding='utf-8').read()

# 1) 単一行push: lolihypapp / jitsufu
push_pat = re.compile(r"CHAR_TEMPLATES\.female\.push\(\{id:'char_(?:lolihypapp|jitsufu)_s\d+_[^']*'.*?\}\);\n")
s, n1 = push_pat.subn('', s)
print('single-line push removed:', n1)
assert n1 == 120, n1

# 2) 複数行push: window.CHAR_TEMPLATES.female.push({\n\n  id:'char_tousatsu_xxx',... });
#    youchienは存在しないが念のため除外
multi_pat = re.compile(
    r"window\.CHAR_TEMPLATES\.female\.push\(\{\s*\n+\s*id:'char_tousatsu_(?!youchien_)[a-zA-Z0-9_]+'.*?\}\);\n*",
    re.DOTALL)
s, n2 = multi_pat.subn('', s)
print('multi-line tousatsu push removed:', n2)
assert n2 == 9, n2

# 3) グループ定義削除
#  3a) {key:'lolihypapp_sN'/'jitsufu_sN',label:"...",fn:...},
gd1 = re.compile(r"\{key:'(?:lolihypapp|jitsufu)_s\d+',label:\"[^\"]*\",fn:id => /\^char_(?:lolihypapp|jitsufu)_s\d+_/\.test\(id\)(?:,bigGenre:'[^']*')?\},")
s, n3 = gd1.subn('', s)
print('gd lolihypapp/jitsufu removed:', n3)
assert n3 == 20, n3

#  3b) {key:'tousatsu',label:"📷 女湯露天盗撮",fn:id => /^char_tousatsu_/.test(id)},
gd2 = re.compile(r"\{key:'tousatsu',label:\"[^\"]*\",fn:id => /\^char_tousatsu_/\.test\(id\)(?:,bigGenre:'[^']*')?\},\n*")
s, n4 = gd2.subn('', s)
#  3c) { key:'tousatsu', ... match: id => /^char_tousatsu_/.test(id) },（CHAR_CATEGORIES形式・2箇所）
gd3 = re.compile(r"\{\s*key:'tousatsu',\s*label:\"[^\"]*\",\s*match: id => /\^char_tousatsu_/\.test\(id\)\s*\},\n*")
s, n5 = gd3.subn('', s)
#  3d) サブグループ fn:function形式（tousatsu_youjo/shougaku/chuugaku）
gd4 = re.compile(r"\{\s*key:'tousatsu_(?:youjo|shougaku|chuugaku)',\s*label:'[^']*',\s*fn: function\(id\)\{ return /\^char_tousatsu_(?:youjo|shougaku|chuugaku)_/\.test\(id\); \} \},\n*")
s, n6 = gd4.subn('', s)
print('gd tousatsu removed:', n4, n5, n6)
assert n4 >= 1 and n5 >= 1, (n4, n5)

# 4) 残存チェック（除外fn内の否定参照 !/^char_tousatsu_youjo_/ 等とHTML仕様書表は許容）
rest_main = len(re.findall(r"id:'char_(?:lolihypapp|jitsufu)_s\d+_", s))
rest_tou = len(re.findall(r"id:'char_tousatsu_(?!youchien_)", s))
print('remaining char defs:', rest_main, rest_tou)
assert rest_main == 0 and rest_tou == 0

m = re.search(r'name="version" content="(\d+)"', s)
old = m.group(1); new = str(int(old)+1)
s = s.replace(f'content="{old}"', f'content="{new}"', 1)
print('version:', old, '->', new)
open(DB, 'w', encoding='utf-8', newline='').write(s)

# 5) outfit sets
d = json.load(open(OS_JSON, encoding='utf-8'))
keys = ['S0%d' % n for n in list(range(542, 552)) + list(range(622, 632))]
removed = [k for k in keys if d.pop(k, None) is not None]
print('outfit sets removed:', removed)
assert len(removed) == 20, removed
json.dump(d, open(OS_JSON, 'w', encoding='utf-8'), ensure_ascii=False)
print('outfit_sets keys:', len(d))

s2 = open(DB, encoding='utf-8').read()
d2 = json.load(open(OS_JSON, encoding='utf-8'))
assert not re.search(r"id:'char_(?:lolihypapp|jitsufu)_s\d+_", s2)
assert not re.search(r"id:'char_tousatsu_(?!youchien_)", s2)
assert all(k not in d2 for k in keys)
print('VERIFY OK')
