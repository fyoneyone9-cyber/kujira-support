# -*- coding: utf-8 -*-
# 「その他」グループの中身を特定する
# 方式: CHAR_GROUP_DEFS相当の全fn/match/patternの正規表現を抽出し、
#       全キャラIDに対してどれにもマッチしないものを列挙する
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()

# 1) 全キャラID収集
all_ids = sorted(set(re.findall(r"id[\"']?\s*:\s*[\"'](char_[a-zA-Z0-9_]+)[\"']", s)))
print('total char ids:', len(all_ids))

# 2) グループ判定の正規表現を全部収集（fn:id => /.../.test(id) / match: id => /.../ / pattern:/.../）
pats = []
for m in re.finditer(r"(?:fn:\s*id\s*=>|match:\s*id\s*=>)\s*(.+?)(?:\},|\} \},)", s):
    expr = m.group(1)
    for rm in re.finditer(r"/((?:[^/\\\n]|\\.)+)/", expr):
        pats.append(rm.group(1))
for m in re.finditer(r"pattern:\s*/((?:[^/\\\n]|\\.)+)/", s):
    pats.append(m.group(1))
for m in re.finditer(r"fn:\s*function\(id\)\{\s*return\s*/((?:[^/\\\n]|\\.)+)/", s):
    pats.append(m.group(1))
pats = sorted(set(pats))
print('patterns collected:', len(pats))

compiled = []
for p in pats:
    try:
        compiled.append(re.compile(p))
    except re.error:
        pass
print('compiled:', len(compiled))

unmatched = []
for cid in all_ids:
    if not any(c.search(cid) for c in compiled):
        unmatched.append(cid)
print('=== unmatched (sonota) ===', len(unmatched))
for x in unmatched:
    print(' ', x)
