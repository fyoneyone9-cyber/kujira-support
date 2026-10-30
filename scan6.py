# 目的: どのジャンルのシーンvalueが「コピー」か特定。
# 各S-setのvalue配列をジャンル間比較（完全一致 or 高類似）。
import json, collections, hashlib
d = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json', encoding='utf-8'))

# genre -> season -> key  (scan5の結果を再構築)
import re
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()
pairs = re.findall(r"id:\s*['\"](char_[^'\"]+)['\"][^}]*?outfits_ref\s*:\s*['\"]([^'\"]+)['\"]", s)
gmap = collections.defaultdict(dict)
for cid, ref in pairs:
    m = re.search(r'^char_([a-z0-9_]+?)_s(10|[0-9])_', cid)
    if m:
        gmap[m.group(1)][int(m.group(2))] = ref

# 10シーズン揃いのジャンル
full = {g: v for g, v in gmap.items() if len(v) >= 8}
print('genres with >=8 seasons:', len(full))

def vals(key):
    arr = d.get(key, [])
    return [x.get('value','') for x in arr if isinstance(x, dict)]

# ジャンル×シーズンのvalueハッシュ → 同一valueセットのグループ
h2g = collections.defaultdict(list)
for g, seas in sorted(full.items()):
    for sn, key in sorted(seas.items()):
        v = vals(key)
        hh = hashlib.md5(json.dumps(v).encode()).hexdigest()
        h2g[hh].append(f'{g}/S{sn}({key},n={len(v)})')
groups = sorted([v for v in h2g.values() if len(v) > 1], key=len, reverse=True)
out = [f'genres>=8seasons: {sorted(full)}', f'dup groups: {len(groups)}']
for grp in groups:
    out.append(f'[{len(grp)}] ' + ', '.join(grp))
open(r'C:\GensparkClaw\kujira-support\_s6.txt','w',encoding='utf-8').write('\n'.join(out))
print('done, groups:', len(groups))
