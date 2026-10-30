# -*- coding: utf-8 -*-
# ロリコン天国S1-10 削除（140体 + registerGenre10 + outfit sets S0293-S0302）
import re, sys, io, json, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ts = time.strftime('%Y%m%d_%H%M%S')
DB = r'C:\AI\ComfyUI\dashboard.html'
OS_JSON = r'C:\AI\ComfyUI\outfit_sets.json'

db_bak = DB.replace('.html', f'_backup_{ts}_tengokudel.html')
os_bak = OS_JSON.replace('.json', f'_backup_{ts}_tengokudel.json')
shutil.copy2(DB, db_bak); shutil.copy2(OS_JSON, os_bak)
print('backup:', db_bak)
print('backup:', os_bak)

s = open(DB, encoding='utf-8').read()

push_pat = re.compile(r"CHAR_TEMPLATES\.female\.push\(\{id:'char_lolicon_heaven_s\d+_[^']*'.*?\}\);\n")
s, n_push = push_pat.subn('', s)
print('push removed:', n_push)
assert n_push == 140, n_push

reg_pat = re.compile(r"if\(window\.registerGenre\)registerGenre\(\{key:'lolicon_heaven_s\d+'[^\n]*?\}\);\n?")
s, n_reg = reg_pat.subn('', s)
print('registerGenre removed:', n_reg)
assert n_reg == 10, n_reg

# コメントマーカー [LOLICON_SN] も掃除
cm_pat = re.compile(r"// ===== /?\[LOLICON_S\d+\] =====\n?")
s, n_cm = cm_pat.subn('', s)
print('comment markers removed:', n_cm)

# UI選択リストのエントリ {name:'💗ロリコン天国', idpfx:'char_lolicon_heaven_s'}, も削除
ui_pat = re.compile(r"\{name:'[^']*ロリコン天国[^']*',\s*idpfx:'char_lolicon_heaven_s'\},\n*")
s, n_ui = ui_pat.subn('', s)
print('ui list entries removed:', n_ui)

# 残存確認
rest_idx = [m.start() for m in re.finditer(r'lolicon_heaven', s)]
print('remaining occurrences:', len(rest_idx))
for i in rest_idx[:10]:
    print(repr(s[max(0,i-80):i+80]))
    print('---')
assert len(rest_idx) == 0, f'{len(rest_idx)} refs remain'

m = re.search(r'name="version" content="(\d+)"', s)
old = m.group(1); new = str(int(old)+1)
s = s.replace(f'content="{old}"', f'content="{new}"', 1)
print('version:', old, '->', new)
open(DB, 'w', encoding='utf-8', newline='').write(s)

d = json.load(open(OS_JSON, encoding='utf-8'))
keys = ['S0%d' % n for n in range(293, 303)]
removed = [k for k in keys if d.pop(k, None) is not None]
print('outfit sets removed:', removed)
assert len(removed) == 10, removed
json.dump(d, open(OS_JSON, 'w', encoding='utf-8'), ensure_ascii=False)
print('outfit_sets keys:', len(d))

s2 = open(DB, encoding='utf-8').read()
d2 = json.load(open(OS_JSON, encoding='utf-8'))
assert 'lolicon_heaven' not in s2
assert all(k not in d2 for k in keys)
print('VERIFY OK')
