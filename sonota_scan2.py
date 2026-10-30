# -*- coding: utf-8 -*-
# 「その他」の実体特定: UIが使うCHAR_GROUP_DEFS（fn形式GDリスト）のパターンのみで判定し、
# どれにもマッチしないキャラIDを列挙（=UIで「その他」に落ちる集合）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()

# CHAR_GROUP_DEFS本体を特定
i = s.find('CHAR_GROUP_DEFS')
print('CHAR_GROUP_DEFS at', i, repr(s[i-60:i+120])[:220])
# 定義配列の範囲: '= [' から対応する ']'
j = s.find('[', i)
depth = 0
k = j
in_str = None; esc = False
while k < len(s):
    c = s[k]
    if esc: esc = False
    elif c == '\\': esc = True
    elif in_str:
        if c == in_str: in_str = None
    elif c in ('"', "'", '`'): in_str = c
    elif c == '[': depth += 1
    elif c == ']':
        depth -= 1
        if depth == 0:
            break
    k += 1
arr = s[j:k]
print('array len:', len(arr))

# fn:id => /.../.test(id) パターン抽出
pats = []
for m in re.finditer(r"fn:\s*id\s*=>\s*(.+?)(?=,bigGenre|\},)", arr):
    for rm in re.finditer(r"/((?:[^/\\\n]|\\.)+)/", m.group(1)):
        pats.append(rm.group(1))
pats = sorted(set(pats))
print('UI patterns:', len(pats))
compiled = [re.compile(p) for p in pats]

all_ids = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](char_[a-zA-Z0-9_]+)[\"']", s)))
unmatched = [cid for cid in all_ids if not any(c.search(cid) for c in compiled)]
print('=== UI-sonota ===', len(unmatched))
import collections
pref = collections.Counter('_'.join(x.split('_')[:3]) for x in unmatched)
for kk, v in sorted(pref.items(), key=lambda t: -t[1]):
    print(' ', kk, v)
print('--- full list ---')
for x in unmatched:
    print(x)
