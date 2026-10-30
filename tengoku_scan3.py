# -*- coding: utf-8 -*-
# ロリコン天国S push形式・件数・outfits_refを確認（registerGenre形式）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
ids = re.findall(r"push\(\{id:'(char_lolicon_heaven_s\d+_[a-zA-Z0-9_]+)'", s)
print('push total:', len(ids))
rows = re.findall(r"push\(\{id:'(char_lolicon_heaven_s\d+_[a-zA-Z0-9_]+)'[^\n]*?outfits_ref:\"(S\d+)\"", s)
print('with ref:', len(rows))
seen = {}
for a, b in rows:
    seen.setdefault(b, []).append(a)
for b in sorted(seen):
    print(b, len(seen[b]), seen[b][0])
# ref無し
noref = set(ids) - set(a for a,_ in rows)
print('no-ref:', len(noref), sorted(noref)[:5])
# registerGenre行数
regs = re.findall(r"if\(window\.registerGenre\)registerGenre\(\{key:'lolicon_heaven_s\d+'[^\n]*?\}\);", s)
print('registerGenre lines:', len(regs))
# 他の 'lolicon_heaven' 参照
others = [m.start() for m in re.finditer(r'lolicon_heaven', s)]
print('total occurrences:', len(others))
