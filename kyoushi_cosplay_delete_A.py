# -*- coding: utf-8 -*-
# 教師と教え子S1-10(60体) + コスプレ図鑑(31体) 削除
# GD: kyoushi_s1-10(fn形式) + cosplay_zukan/cosplay_zukan_jk(fn形式・複数行bigGenre形式・registerGenre形式)
# outfit sets: S0562-S0571(kyoushi) + cosplay専用ref(S0165,S0166,S0168等は実体確認後に削除)
import re, sys, io, json, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ts = time.strftime('%Y%m%d_%H%M%S')
DB = r'C:\AI\ComfyUI\dashboard.html'
OS_JSON = r'C:\AI\ComfyUI\outfit_sets.json'

db_bak = DB.replace('.html', f'_backup_{ts}_kcdel.html')
os_bak = OS_JSON.replace('.json', f'_backup_{ts}_kcdel.json')
shutil.copy2(DB, db_bak); shutil.copy2(OS_JSON, os_bak)
print('backup:', db_bak)
print('backup:', os_bak)

s = open(DB, encoding='utf-8').read()
orig_len = len(s)

TARGET = re.compile(r"char_(?:kyoushi_s\d+_[a-zA-Z0-9_]+|cosplay_zukan_[a-zA-Z0-9_]+)")

def find_obj_bounds(s, id_pos):
    i = id_pos
    depth = 0
    start = -1
    while i > 0:
        c = s[i]
        if c == '}':
            depth += 1
        elif c == '{':
            if depth == 0:
                start = i
                break
            depth -= 1
        i -= 1
    assert start >= 0
    j = start
    depth = 0
    in_str = None
    esc = False
    while j < len(s):
        c = s[j]
        if esc:
            esc = False
        elif c == '\\':
            esc = True
        elif in_str:
            if c == in_str:
                in_str = None
        elif c in ('"', "'", '`'):
            in_str = c
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                j += 1
                break
        j += 1
    end = j
    pre = s[max(0, start-80):start]
    m = re.search(r"(?:window\.)?CHAR_TEMPLATES\.female\.push\(\s*$", pre)
    if m:
        start = start - (len(pre) - m.start())
        k = end
        while k < len(s) and s[k] in ' \n\r\t':
            k += 1
        if s[k:k+2] == ');':
            end = k + 2
    else:
        k = end
        while k < len(s) and s[k] in ' \n\r\t':
            k += 1
        if k < len(s) and s[k] == ',':
            end = k + 1
    if end < len(s) and s[end] == '\n':
        end += 1
    return start, end

removed_ids = []
while True:
    m = re.search(r"id[\"']?\s*:\s*[\"'](" + TARGET.pattern + r")[\"']", s)
    if not m:
        break
    cid = m.group(1)
    assert TARGET.fullmatch(cid), cid
    st, en = find_obj_bounds(s, m.start())
    seg = s[st:en]
    other = [x for x in re.findall(r"id[\"']?\s*:\s*[\"'](char_[a-zA-Z0-9_]+)[\"']", seg) if x != cid]
    assert not other, (cid, other[:3])
    s = s[:st] + s[en:]
    removed_ids.append(cid)
print('chars removed:', len(removed_ids))
import collections
cnt = collections.Counter('kyoushi' if x.startswith('char_kyoushi_') else 'cosplay' for x in removed_ids)
print('breakdown:', dict(cnt))
dup = [x for x, c in collections.Counter(removed_ids).items() if c > 1]
print('duplicated ids (defined multiple times):', dup[:10])
assert 90 <= len(removed_ids) <= 110, len(removed_ids)

# GD削除
tot = 0
# fn形式（bigGenre付き）
s, n = re.subn(r"\{key:'(?:kyoushi_s\d+|cosplay_zukan|cosplay_zukan_jk)',label:\"[^\"]*\",fn:id => [^\n]*?,bigGenre:'[^']*'\},\n*", '', s)
tot += n; print('gd fn removed:', n)
# registerGenre形式
s, n = re.subn(r"(?:if\(window\.registerGenre\))?registerGenre\(\{key:'(?:cosplay_zukan|cosplay_zukan_jk|kyoushi_s\d+)'[^\n]*?\}\);\n*", '', s)
tot += n; print('registerGenre removed:', n)
# 複数行 bigGenre オブジェクト形式（cosplay_zukan_jk）
s, n = re.subn(r"\{\s*key:'cosplay_zukan_jk',\s*label:'[^']*',\s*bigGenre:'[^']*',[^}]*\},?\n*", '', s)
tot += n; print('gd multiline removed:', n)
# match/function形式
s, n = re.subn(r"\{\s*key:\s*'(?:kyoushi_s\d+|cosplay_zukan|cosplay_zukan_jk)',\s*label:\s*[\"'][^\"']*[\"'],\s*(?:match|fn)[^\n]*?\}\s*,?\n*", '', s)
tot += n; print('gd match/fn removed:', n)
print('total gd removed:', tot)

# 残存チェック
rest = re.findall(r"id[\"']?\s*:\s*[\"'](" + TARGET.pattern + r")[\"']", s)
assert len(rest) == 0, rest[:5]
rest2 = len(re.findall(r"'(?:kyoushi_s\d+|cosplay_zukan(?:_jk)?)'", s))
print('remaining key refs:', rest2)

m = re.search(r'name="version" content="(\d+)"', s)
old = m.group(1); new = str(int(old)+1)
s = s.replace(f'content="{old}"', f'content="{new}"', 1)
print('version:', old, '->', new)
open(DB, 'w', encoding='utf-8', newline='').write(s)
print('saved. size:', orig_len, '->', len(s))

# outfit sets: kyoushi S0562-S0571 + cosplay専用（使用者が全てcosplayだったもののみ）
d = json.load(open(OS_JSON, encoding='utf-8'))
keys = ['S0%d' % n for n in range(562, 572)]
# cosplay専用ref候補: 保存後のdashboardに参照が残っていないセットのみ削除
for cand in ['S0165', 'S0166', 'S0167', 'S0168']:
    if cand in d and ('outfits_ref:"%s"' % cand) not in s and ("outfits_ref:'%s'" % cand) not in s:
        keys.append(cand)
removed = [k for k in keys if d.pop(k, None) is not None]
print('outfit sets removed:', removed)
json.dump(d, open(OS_JSON, 'w', encoding='utf-8'), ensure_ascii=False)
print('outfit_sets keys:', len(d))
print('VERIFY OK')
