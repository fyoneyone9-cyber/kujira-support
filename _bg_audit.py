# -*- coding: utf-8 -*-
import io, re, sys, collections
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
t = io.open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
i = t.find('CHAR_GROUP_DEFS = [')
e = t.find('];', i)
seg = t[i:e]
pat = re.compile(r"""\{key:\s*'([^']+)'\s*,\s*label:\s*(?:'([^']*)'|"([^"]*)")(.*?)\}""")
cnt = collections.Counter()
nobg = []
rows = []
for m in pat.finditer(seg):
    k = m.group(1); lab = m.group(2) or m.group(3); rest = m.group(4)
    bm = re.search(r"""bigGenre:\s*(?:'([^']*)'|"([^"]*)")""", rest)
    bg = (bm.group(1) or bm.group(2)) if bm else ''
    rows.append((k, lab, bg))
    if bg: cnt[bg] += 1
    else: nobg.append((k, lab))
print('total defs:', len(rows))
print('--- bigGenre分布 ---')
for bg, n in cnt.most_common(): print(f'{n:4d}  {bg}')
print('--- bigGenreなし:', len(nobg))
for k, l in nobg: print(k, '|', l)
