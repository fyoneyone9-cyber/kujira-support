# -*- coding: utf-8 -*-
# 改造ジブリール(6)+改造ティファv2(1)+改造2Bv2(1)+改造ミクv2(1)+改造歌手v2(4)+改造テイラーv2(1)=14体削除
# 世界DUO改造済み(char_sekai_duo_kaizou_)は対象外・無傷確認
import re, sys, io, os, json, shutil, time, subprocess, tempfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ts = time.strftime('%Y%m%d_%H%M%S')
DB = r'C:\AI\ComfyUI\dashboard.html'
OS_JSON = r'C:\AI\ComfyUI\outfit_sets.json'
db_bak = DB.replace('.html', f'_backup_{ts}_kaizov2del.html')
os_bak = OS_JSON.replace('.json', f'_backup_{ts}_kaizov2del.json')
shutil.copy2(DB, db_bak); shutil.copy2(OS_JSON, os_bak)
print('backup:', db_bak)
print('backup:', os_bak)

s = open(DB, encoding='utf-8').read()
orig_len = len(s)

TARGET = re.compile(r"char_kaizo_(?:jibril_[A-F]|tifa_v2|2b_v2|miku_v2|singer_[a-z]+_v2|taylor_v2)")

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
    m = re.search(r"(?:window\.)?CHAR_TEMPLATES\.(?:female|male)\.push\(\s*$", pre)
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
print('chars removed:', len(removed_ids), 'unique:', len(set(removed_ids)))
assert len(set(removed_ids)) == 14, sorted(set(removed_ids))

# 空push残骸除去
s, n_empty = re.subn(r"(?:window\.)?CHAR_TEMPLATES\.(?:female|male)\.push\(\s*\);\n*", '', s)
print('empty push removed:', n_empty)

# GD削除
keys = r"(?:kaizo_jibril|kaizo_tifa_v2|kaizo_2b_v2|kaizo_miku_v2|kaizo_singer_v2|kaizo_taylor_v2)"
tot = 0
s, n = re.subn(r"\{key:'" + keys + r"',label:\"[^\"]*\",fn:id => [^\n]*?,bigGenre:'[^']*'\},\n*", '', s)
tot += n; print('gd fn removed:', n)
s, n = re.subn(r"\{\s*key:\s*'" + keys + r"',\s*label:\s*[\"'][^\"']*[\"'],\s*match: id => [^\n]*?\}\s*,?\n*", '', s)
tot += n; print('gd match removed:', n)
s, n = re.subn(r"\{\s*key:\s*'" + keys + r"',\s*label:\s*'[^']*',\s*fn: function\(id\)\{[^\n]*?\}\s*\},?\n*", '', s)
tot += n; print('gd function removed:', n)
s, n = re.subn(r"(?:if\(window\.registerGenre\))?registerGenre\(\{key:'" + keys + r"'[^\n]*?\}\);\n*", '', s)
tot += n; print('registerGenre removed:', n)
print('total gd removed:', tot)

# 世界DUO改造済みが無傷か
assert "char_sekai_duo_kaizou_" in s, 'sekai_duo_kaizou should remain'
rest = re.findall(r"id[\"']?\s*:\s*[\"'](" + TARGET.pattern + r")[\"']", s)
assert len(rest) == 0, rest[:5]

# 全scriptブロック構文検証（恒久対策）
def check_all(src):
    tmpdir = tempfile.mkdtemp()
    bad = []
    for i, m in enumerate(re.finditer(r'<script(?:\s[^>]*)?>(.*?)</script>', src, re.DOTALL)):
        body = m.group(1)
        if len(body.strip()) < 10:
            continue
        p = os.path.join(tmpdir, f'b{i}.js')
        open(p, 'w', encoding='utf-8').write(body)
        r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
        if r.returncode != 0:
            em = re.search(r'\.js:(\d+)', r.stderr)
            bad.append((i, src[:m.start()].count('\n')+1, int(em.group(1)) if em else -1, r.stderr[:200]))
    return bad

for attempt in range(5):
    bad = check_all(s)
    print('attempt', attempt, 'bad blocks:', len(bad))
    if not bad:
        break
    blk_idx, html_line, js_line, err = bad[0]
    lines = s.split('\n')
    target_line = html_line + js_line - 1
    tok = lines[target_line-1].strip()
    print('  bad token at html line', target_line, repr(tok))
    assert tok in (');', '},', '}', ',', ';'), ('unexpected', tok, err)
    del lines[target_line-1]
    s = '\n'.join(lines)
assert not bad

m = re.search(r'name="version" content="(\d+)"', s)
old = m.group(1); new = str(int(old)+1)
s = s.replace(f'content="{old}"', f'content="{new}"', 1)
print('version:', old, '->', new)
open(DB, 'w', encoding='utf-8', newline='').write(s)
print('saved. size:', orig_len, '->', len(s), 'ALL SCRIPT BLOCKS OK')

# outfit sets: S0054(ジブリール専用), S0030は他参照残ってたら残す
d = json.load(open(OS_JSON, encoding='utf-8'))
removed_sets = []
for r in ['S0054', 'S0030']:
    if r in d and ('outfits_ref:"%s"' % r) not in s and ("outfits_ref:'%s'" % r) not in s:
        del d[r]
        removed_sets.append(r)
print('outfit sets removed:', removed_sets)
json.dump(d, open(OS_JSON, 'w', encoding='utf-8'), ensure_ascii=False)
print('outfit_sets keys:', len(d))
print('DONE')
