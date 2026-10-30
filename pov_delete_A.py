# -*- coding: utf-8 -*-
# POV 9グループ削除（char_pov_ 142体 + GD各形式 + grp_pov + registerGenre + S0119）
# 注意: char_hyoi_shougaku_G_pov（憑依キャラ）と cp_all（コラボPOV）は対象外
import re, sys, io, json, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ts = time.strftime('%Y%m%d_%H%M%S')
DB = r'C:\AI\ComfyUI\dashboard.html'
OS_JSON = r'C:\AI\ComfyUI\outfit_sets.json'

db_bak = DB.replace('.html', f'_backup_{ts}_povdel.html')
os_bak = OS_JSON.replace('.json', f'_backup_{ts}_povdel.json')
shutil.copy2(DB, db_bak); shutil.copy2(OS_JSON, os_bak)
print('backup:', db_bak)
print('backup:', os_bak)

s = open(DB, encoding='utf-8').read()

# 1) push削除（単一行・複数行両対応、DOTALLで }); まで）
push_pat = re.compile(
    r"(?:window\.)?CHAR_TEMPLATES\.female\.push\(\{\s*\n*\s*id:\s*['\"]char_pov_[a-zA-Z0-9_]+['\"].*?\}\);\n*",
    re.DOTALL)
s, n_push = push_pat.subn('', s)
print('push removed:', n_push)
assert n_push == 142, n_push

# 2) GD形式1: {key:'pov_xxx',label:"...",fn:id => ...},（fn本体に改行なし・bigGenre付き）
gd1 = re.compile(r"\{key:'(?:pov_normal|pov_sailor|pov_yuri|pov_chikan|pov_rape|pov_panchira|pov_pinsaro|pov_deliheru|pov_all|pov_mirror)',label:\"[^\"]*\",fn:id => [^\n]*?(?:,bigGenre:'[^']*')?\},\n*")
s, n1 = gd1.subn('', s)
print('gd fn-style removed:', n1)

# 3) GD形式2: { key:'pov_xxx', label:"...", match: id => ... },
gd2 = re.compile(r"\{\s*key:'(?:pov_normal|pov_sailor|pov_yuri|pov_chikan|pov_rape|pov_panchira|pov_pinsaro|pov_deliheru|pov_mirror)',\s*label:[\"'][^\"']*[\"'],\s*match: id => [^\n]*?\},\n*")
s, n2 = gd2.subn('', s)
print('gd match-style removed:', n2)

# 4) GD形式3: { key:'pov', label:'...', fn: function(id){...} },
gd3 = re.compile(r"\{\s*key:'pov',\s*label:'[^']*',\s*fn: function\(id\)\{ return /char_pov_/\.test\(id\); \} \},\n*")
s, n3 = gd3.subn('', s)
print('gd function-style removed:', n3)

# 5) registerGenre pov行
gd4 = re.compile(r"registerGenre\(\{key:'pov',label:'[^']*',pattern:/char_pov_/,categoryGroup:'grp_pov'\}\);\n*")
s, n4 = gd4.subn('', s)
print('registerGenre removed:', n4)

# 6) grp_pov 大グループ定義: { key:'grp_pov', label:..., cats:[...] },
gd5 = re.compile(r"\{\s*key:'grp_pov',\s*label:\"[^\"]*\",\s*icon:'[^']*',\s*\n*\s*cats:\[[^\]]*\]\s*\},\n*")
s, n5 = gd5.subn('', s)
print('grp_pov removed:', n5)

# 7) 残存チェック: char_pov_ の定義が残っていないこと（除外: hyoi pov・GD内の否定参照が残る場合は表示）
rest = [m.start() for m in re.finditer(r'char_pov_', s)]
print('remaining char_pov_ occurrences:', len(rest))
for i in rest[:12]:
    print(repr(s[max(0,i-70):i+70])[:170])
    print('---')
# id定義としての残存は0必須
assert not re.search(r"id:\s*['\"]char_pov_", s), 'char def remains'

m = re.search(r'name="version" content="(\d+)"', s)
old = m.group(1); new = str(int(old)+1)
s = s.replace(f'content="{old}"', f'content="{new}"', 1)
print('version:', old, '->', new)
open(DB, 'w', encoding='utf-8', newline='').write(s)

# 8) outfit set S0119（POV専用と確認済み）
d = json.load(open(OS_JSON, encoding='utf-8'))
if 'S0119' in d:
    del d['S0119']
    print('outfit set removed: S0119')
json.dump(d, open(OS_JSON, 'w', encoding='utf-8'), ensure_ascii=False)
print('outfit_sets keys:', len(d))

s2 = open(DB, encoding='utf-8').read()
assert not re.search(r"id:\s*['\"]char_pov_", s2)
print('VERIFY OK')
