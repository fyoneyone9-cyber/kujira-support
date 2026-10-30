# -*- coding: utf-8 -*-
# 工場シリーズ char_factory_* 20体 + GD2件 + S0169 削除、block25の壊れ残骸も一掃
# 方式: 括弧対応でオブジェクト削除 → 空push残骸 'push(\s*);' を除去 → 孤立');'除去 → 全scriptブロックnode --check → OKなら保存
import re, sys, io, os, json, shutil, time, subprocess, tempfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ts = time.strftime('%Y%m%d_%H%M%S')
DB = r'C:\AI\ComfyUI\dashboard.html'
OS_JSON = r'C:\AI\ComfyUI\outfit_sets.json'
db_bak = DB.replace('.html', f'_backup_{ts}_factorydel.html')
os_bak = OS_JSON.replace('.json', f'_backup_{ts}_factorydel.json')
shutil.copy2(DB, db_bak); shutil.copy2(OS_JSON, os_bak)
print('backup:', db_bak)
print('backup:', os_bak)

s = open(DB, encoding='utf-8').read()
orig_len = len(s)

TARGET = re.compile(r"char_factory_[a-zA-Z0-9_]+")

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
    st, en = find_obj_bounds(s, m.start())
    seg = s[st:en]
    other = [x for x in re.findall(r"id[\"']?\s*:\s*[\"'](char_[a-zA-Z0-9_]+)[\"']", seg) if x != cid]
    assert not other, (cid, other[:3])
    s = s[:st] + s[en:]
    removed_ids.append(cid)
print('chars removed:', len(removed_ids))
import collections
dup = [x for x, c in collections.Counter(removed_ids).items() if c > 1]
print('unique:', len(set(removed_ids)), 'duplicated defs:', dup[:10])
for x in removed_ids:
    assert TARGET.fullmatch(x), x
assert 20 <= len(removed_ids) <= 40, len(removed_ids)

# 空push残骸: 'window.CHAR_TEMPLATES.female.push(\n\n  );' のような空呼び出しを除去
s, n_empty = re.subn(r"(?:window\.)?CHAR_TEMPLATES\.(?:female|male)\.push\(\s*\);\n*", '', s)
print('empty push removed:', n_empty)
# 孤立 ');' 行（push(が既に消えて残った閉じ）を除去
lines = s.split('\n')
orphans = [i for i, l in enumerate(lines) if l.strip() == ');']
# 前方の非空行がオブジェクト/push系でない孤立のみ削除は危険 → node --checkで判断するため一旦そのまま

# GD削除
tot = 0
s, n = re.subn(r"\{key:'factory',label:\"[^\"]*\",fn:id => /\^char_factory_/\.test\(id\)(?:,bigGenre:'[^']*')?\},\n*", '', s)
tot += n; print('gd fn removed:', n)
s, n = re.subn(r"(?:if\(window\.registerGenre\))?registerGenre\(\{key:'factory'[^\n]*?\}\);\n*", '', s)
tot += n; print('registerGenre removed:', n)
print('total gd removed:', tot)

rest = re.findall(r"char_factory_", s)
print('remaining factory refs:', len(rest))

# 全scriptブロック検証（孤立');'が残っていればここで検出 → 該当行を特定して除去を試みる）
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
            # jsエラー行を抽出
            em = re.search(r'\.js:(\d+)', r.stderr)
            bad.append((i, src[:m.start()].count('\n')+1, int(em.group(1)) if em else -1, r.stderr[:200]))
    return bad

for attempt in range(5):
    bad = check_all(s)
    print('attempt', attempt, 'bad blocks:', len(bad))
    if not bad:
        break
    # 壊れブロックのエラー行が孤立トークン(');' '},' '}' ',' ';')なら除去して再試行
    blk_idx, html_line, js_line, err = bad[0]
    lines = s.split('\n')
    target_line = html_line + js_line - 1  # 1-index
    tok = lines[target_line-1].strip()
    print('  bad token at html line', target_line, repr(tok))
    assert tok in (');', '},', '}', ',', ';'), ('unexpected token', tok, err)
    del lines[target_line-1]
    s = '\n'.join(lines)
assert not bad, 'still broken after cleanup'

m = re.search(r'name="version" content="(\d+)"', s)
old = m.group(1); new = str(int(old)+1)
s = s.replace(f'content="{old}"', f'content="{new}"', 1)
print('version:', old, '->', new)
open(DB, 'w', encoding='utf-8', newline='').write(s)
print('saved. size:', orig_len, '->', len(s), 'ALL SCRIPT BLOCKS OK')

# outfit set S0169（他に参照者がいなければ削除）
d = json.load(open(OS_JSON, encoding='utf-8'))
if 'S0169' in d and 'outfits_ref:"S0169"' not in s and "outfits_ref:'S0169'" not in s:
    del d['S0169']
    print('outfit set removed: S0169')
json.dump(d, open(OS_JSON, 'w', encoding='utf-8'), ensure_ascii=False)
print('outfit_sets keys:', len(d))
print('DONE')
