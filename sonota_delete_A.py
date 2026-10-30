# -*- coding: utf-8 -*-
# 「その他」80体削除:
#  A) idOverride形式 30体（"idOverride":"char_tentacle_(youjo|shougaku|chuugaku|nurse|nyuuji)_X" を含む配列オブジェクト）
#  B) 日本語名ID 50体（char_(youjo|shougaku)_(flat|small|medium|large|huge)_○○）
import re, sys, io, os, json, shutil, time, subprocess, tempfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ts = time.strftime('%Y%m%d_%H%M%S')
DB = r'C:\AI\ComfyUI\dashboard.html'
db_bak = DB.replace('.html', f'_backup_{ts}_sonotadel.html')
shutil.copy2(DB, db_bak)
print('backup:', db_bak)

s = open(DB, encoding='utf-8').read()
orig_len = len(s)

def find_obj_bounds(s, pos):
    i = pos
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

# A) idOverride オブジェクト削除
n_ov = 0
while True:
    m = re.search(r'"idOverride":\s*"char_tentacle_(?:youjo|shougaku|chuugaku|nurse|nyuuji)_[A-F]"', s)
    if not m:
        break
    st, en = find_obj_bounds(s, m.start())
    seg = s[st:en]
    assert '"idOverride"' in seg
    s = s[:st] + s[en:]
    n_ov += 1
print('idOverride objects removed:', n_ov)
assert n_ov == 30, n_ov

# B) 日本語名ID削除
n_jp = 0
while True:
    m = re.search(r"id:\s*'(char_(?:youjo|shougaku)_(?:flat|small|medium|large|huge)_[^']+)'", s)
    if not m:
        break
    st, en = find_obj_bounds(s, m.start())
    s = s[:st] + s[en:]
    n_jp += 1
print('japanese-id chars removed:', n_jp)
assert n_jp == 50, n_jp

s, n_empty = re.subn(r"(?:window\.)?CHAR_TEMPLATES\.(?:female|male)\.push\(\s*\);\n*", '', s)
print('empty push removed:', n_empty)

# 残存確認
assert not re.search(r'"idOverride":\s*"char_tentacle_(?:youjo|shougaku|chuugaku|nurse|nyuuji)_', s)
assert not re.search(r"id:\s*'char_(?:youjo|shougaku)_(?:flat|small|medium|large|huge)_", s)

# 全scriptブロック構文検証
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
print('DONE')
