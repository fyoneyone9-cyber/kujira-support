# -*- coding: utf-8 -*-
# A案: 巫女穢しS1-S10 削除
# 対象: dashboard.html の push 60行 + グループ定義 {key:'miko_sN',...} 10個
#       outfit_sets.json の S0572〜S0581
# 安全策: 両ファイルをタイムスタンプ付きバックアップ→編集→検証（残存0件・構造チェック）
import re, sys, io, json, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ts = time.strftime('%Y%m%d_%H%M%S')

DB = r'C:\AI\ComfyUI\dashboard.html'
OS_JSON = r'C:\AI\ComfyUI\outfit_sets.json'

# --- backup ---
db_bak = DB.replace('.html', f'_backup_{ts}_mikoA.html')
os_bak = OS_JSON.replace('.json', f'_backup_{ts}_mikoA.json')
shutil.copy2(DB, db_bak)
shutil.copy2(OS_JSON, os_bak)
print('backup:', db_bak)
print('backup:', os_bak)

s = open(DB, encoding='utf-8').read()
orig_len = len(s)

# 1) push行削除（行単位: CHAR_TEMPLATES.female.push({id:'char_miko_sN_...'...});\n）
push_pat = re.compile(r"CHAR_TEMPLATES\.female\.push\(\{id:'char_miko_s\d+_[^']*'.*?\}\);\n")
s, n_push = push_pat.subn('', s)
print('push removed:', n_push)
assert n_push == 60, f'expected 60 push, got {n_push}'

# 2) グループ定義オブジェクト削除: {key:'miko_sN',label:"...",fn:id => /^char_miko_sN_/.test(id)},
gd_pat = re.compile(r"\{key:'miko_s\d+',label:\"[^\"]*\",fn:id => /\^char_miko_s\d+_/\.test\(id\)\},")
s, n_gd = gd_pat.subn('', s)
print('groupdef removed:', n_gd)
assert n_gd == 10, f'expected 10 groupdefs, got {n_gd}'

# 3) 残存チェック
rest = s.count('char_miko_s') + len(re.findall(r"'miko_s\d+'", s)) + len(re.findall(r'"miko_s\d+"', s))
print('remaining refs:', rest)
assert rest == 0, 'remaining refs found'

# 4) version +1
m = re.search(r'name="version" content="(\d+)"', s)
if m:
    old = m.group(1)
    new = str(int(old) + 1)
    s = s.replace(f'content="{old}"', f'content="{new}"', 1)
    print('version:', old, '->', new)

open(DB, 'w', encoding='utf-8', newline='').write(s)
print('dashboard saved. size:', orig_len, '->', len(s))

# 5) outfit_sets.json から S0572〜S0581 削除
d = json.load(open(OS_JSON, encoding='utf-8'))
removed = []
for n in range(572, 582):
    k = 'S0%d' % n
    if k in d:
        del d[k]
        removed.append(k)
print('outfit sets removed:', removed)
assert len(removed) == 10
json.dump(d, open(OS_JSON, 'w', encoding='utf-8'), ensure_ascii=False)
print('outfit_sets.json saved. keys:', len(d))

# 6) 再検証: 読み直してゼロ確認
s2 = open(DB, encoding='utf-8').read()
d2 = json.load(open(OS_JSON, encoding='utf-8'))
assert 'char_miko_s' not in s2
assert all(('S0%d' % n) not in d2 for n in range(572, 582))
print('VERIFY OK: all miko S1-S10 refs removed')
