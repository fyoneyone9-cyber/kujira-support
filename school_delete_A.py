# -*- coding: utf-8 -*-
# 画像全グループ削除: 小学生(学年別含む)/幼女・幼児汎用/幼女/まんこ図鑑/保健体育(PE/触手含む)/カルト教団S1-10
# 対象外: char_shougaku_boy_（小学生男子・画像に無し）
import re, sys, io, json, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ts = time.strftime('%Y%m%d_%H%M%S')
DB = r'C:\AI\ComfyUI\dashboard.html'
OS_JSON = r'C:\AI\ComfyUI\outfit_sets.json'
db_bak = DB.replace('.html', f'_backup_{ts}_schooldel.html')
os_bak = OS_JSON.replace('.json', f'_backup_{ts}_schooldel.json')
shutil.copy2(DB, db_bak); shutil.copy2(OS_JSON, os_bak)
print('backup:', db_bak)
print('backup:', os_bak)

s = open(DB, encoding='utf-8').read()
orig_len = len(s)

TARGET = re.compile(
    r"char_(?:"
    r"shougaku_(?!boy_)[a-zA-Z0-9_]+"
    r"|youchien_[a-zA-Z0-9_]+"
    r"|youjo_[a-zA-Z0-9_]+"
    r"|zukan_[a-zA-Z0-9_]+"
    r"|hoken_[a-zA-Z0-9_]+"
    r"|shuukyou_s\d+_[a-zA-Z0-9_]+"
    r")")

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
removed_refs = set()
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
    for r in re.findall(r"outfits_ref:[\"'](S\d+)[\"']", seg):
        removed_refs.add(r)
    s = s[:st] + s[en:]
    removed_ids.append(cid)

import collections
cnt = collections.Counter()
for x in removed_ids:
    cnt[re.match(r'char_([a-z]+)_', x).group(1)] += 1
print('chars removed:', len(removed_ids), dict(cnt))
assert 180 <= len(removed_ids) <= 230, len(removed_ids)
# boy残存確認
assert re.search(r"id[\"']?\s*:\s*[\"']char_shougaku_boy_", s), 'boy should remain'

# GD削除（fn形式bigGenre付き / match形式 / function形式）
tot = 0
keys = r"(?:gakurei|youjo_gen|youjo|shogaku|zukan_all|hoken|hoken_tent|hoken_pe_general|hoken_pe_sailor|hoken_pe_ff|shuukyou_s\d+)"
s, n = re.subn(r"\{key:'" + keys + r"',label:\"[^\"]*\",fn:id => [^\n]*?,bigGenre:'[^']*'\},\n*", '', s)
tot += n; print('gd fn removed:', n)
s, n = re.subn(r"\{\s*key:\s*'" + keys + r"',\s*label:\s*[\"'][^\"']*[\"'],\s*match: id => [^\n]*?\}\s*,?\n*", '', s)
tot += n; print('gd match removed:', n)
s, n = re.subn(r"\{\s*key:\s*'" + keys + r"',\s*label:\s*'[^']*',\s*fn: function\(id\)\{[^\n]*?\} \},\n*", '', s)
tot += n; print('gd function removed:', n)
s, n = re.subn(r"(?:if\(window\.registerGenre\))?registerGenre\(\{key:'" + keys + r"'[^\n]*?\}\);\n*", '', s)
tot += n; print('registerGenre removed:', n)
print('total gd removed:', tot)

rest = re.findall(r"id[\"']?\s*:\s*[\"'](" + TARGET.pattern + r")[\"']", s)
assert len(rest) == 0, rest[:5]

m = re.search(r'name="version" content="(\d+)"', s)
old = m.group(1); new = str(int(old)+1)
s = s.replace(f'content="{old}"', f'content="{new}"', 1)
print('version:', old, '->', new)
open(DB, 'w', encoding='utf-8', newline='').write(s)
print('saved. size:', orig_len, '->', len(s))

# outfit sets: 削除キャラが参照していたrefのうち、保存後に誰も参照していないものだけ削除
d = json.load(open(OS_JSON, encoding='utf-8'))
removed_sets = []
for r in sorted(removed_refs):
    if r in d and ('outfits_ref:"%s"' % r) not in s and ("outfits_ref:'%s'" % r) not in s:
        del d[r]
        removed_sets.append(r)
print('outfit sets removed:', removed_sets)
json.dump(d, open(OS_JSON, 'w', encoding='utf-8'), ensure_ascii=False)
print('outfit_sets keys:', len(d))
print('VERIFY OK')
