# -*- coding: utf-8 -*-
# 大ジャンル3つ（学年・職業／アニメ・芸能／アニメ・芸能・コラボ）配下を全削除
# キャラ: ff_/ff7_/ff8_/ff10_/ff13_/sailor_/tuxedo_mask/incubus_/kimetsu_/loracheck_/chibi_moon2/sensei
# GD: bigGenreが該当3種の全エントリ + match/function形式の同キー + sensei_chars
import re, sys, io, json, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ts = time.strftime('%Y%m%d_%H%M%S')
DB = r'C:\AI\ComfyUI\dashboard.html'
db_bak = DB.replace('.html', f'_backup_{ts}_big3del.html')
shutil.copy2(DB, db_bak)
print('backup:', db_bak)

s = open(DB, encoding='utf-8').read()
orig_len = len(s)

TARGET = re.compile(
    r"char_(?:ff_(?:tifa|aerith|lightning|yuna)"
    r"|ff7_[a-zA-Z0-9_]+|ff8_[a-zA-Z0-9_]+|ff10_[a-zA-Z0-9_]+|ff13_[a-zA-Z0-9_]+"
    r"|sailor_[a-zA-Z0-9_]+"
    r"|tuxedo_mask"
    r"|incubus_[a-zA-Z0-9_]+"
    r"|kimetsu_[a-zA-Z0-9_]+"
    r"|loracheck_[a-zA-Z0-9_]+"
    r"|chibi_moon2"
    r"|sensei"
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
# 内訳を表示して検証（全てTARGET完全一致は削除ループ内で保証済み）
import collections
cnt = collections.Counter()
for x in removed_ids:
    key = re.match(r'char_(ff_|ff7_|ff8_|ff10_|ff13_|sailor_|tuxedo|incubus_|kimetsu_|loracheck_|chibi_moon2|sensei)', x).group(1)
    cnt[key] += 1
for k, v in sorted(cnt.items()):
    print('  breakdown:', k, v)
assert 70 <= len(removed_ids) <= 130, len(removed_ids)

# GD削除1: bigGenreが該当3種のfn形式エントリ全部
gd1 = re.compile(r"\{key:'[^']+',label:\"[^\"]*\",fn:id => [^\n]*?,bigGenre:'[^']*(?:学年・職業|アニメ・芸能)[^']*'\},\n*")
s, n1 = gd1.subn('', s)
print('gd bigGenre removed:', n1)

# GD削除2: match/function形式の同キー（kimetsu/sailor/ff/ff_named/tuxedo/incubus/loracheck/chibi_moon2/cp_*/anime_*/celeb/idol_akb/heroine/legal_*/sensei_chars）
keys = r"(?:ff_named|kimetsu|sailor|ff|tuxedo|incubus|lora_check|loracheck|chibi_moon2|cp_[a-z0-9_]+|anime_cls|anime_mod|celeb|idol_akb|heroine|legal_eva|legal_sailor|legal_ff|legal_kimetsu|sensei_chars)"
gd2 = re.compile(r"\{\s*key:\s*'" + keys + r"',\s*label:\s*[\"'][^\"']*[\"'],\s*(?:match|fn)[^\n]*?\}\s*,?\n*")
s, n2 = gd2.subn('', s)
print('gd match/fn removed:', n2)

# GD削除3: registerGenre sensei_chars
gd3 = re.compile(r"(?:if\(window\.registerGenre\))?registerGenre\(\{key:'sensei_chars'[^\n]*?\}\);\n*")
s, n3 = gd3.subn('', s)
print('registerGenre sensei removed:', n3)

# GD削除4: 複数行 { key:'sensei_chars', label:..., bigGenre:..., ... } 形式
gd4 = re.compile(r"\{\s*key:'sensei_chars',\s*label:'[^']*',\s*bigGenre:'[^']*',[^}]*\},?\n*")
s, n4 = gd4.subn('', s)
print('gd sensei multiline removed:', n4)

# 残存id定義チェック
rest = re.findall(r"id[\"']?\s*:\s*[\"'](" + TARGET.pattern + r")[\"']", s)
print('remaining char defs:', len(rest), rest[:5])
assert len(rest) == 0

m = re.search(r'name="version" content="(\d+)"', s)
old = m.group(1); new = str(int(old)+1)
s = s.replace(f'content="{old}"', f'content="{new}"', 1)
print('version:', old, '->', new)
open(DB, 'w', encoding='utf-8', newline='').write(s)
print('saved. size:', orig_len, '->', len(s))
for x in sorted(removed_ids):
    print('  removed:', x)
