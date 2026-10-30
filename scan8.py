# 目的: dict形式(items)対応で、ジャンル間のシーンvalue重複を正確に測定
import json, re, collections, hashlib
d = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json', encoding='utf-8'))
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()
pairs = re.findall(r"id:\s*['\"](char_[^'\"]+)['\"][^}]*?outfits_ref\s*:\s*['\"]([^'\"]+)['\"]", s)
gmap = collections.defaultdict(dict)
for cid, ref in pairs:
    m = re.search(r'^char_([a-z0-9_]+?)_s(10|[1-9])_', cid)
    if m:
        gmap[m.group(1)][int(m.group(2))] = ref
full = {g: v for g, v in gmap.items() if len(v) >= 8}

def vals(key):
    a = d.get(key)
    if isinstance(a, dict):
        a = a.get('items', [])
    if not isinstance(a, list):
        return []
    return [x.get('value', '') for x in a if isinstance(x, dict)]

h2g = collections.defaultdict(list)
for g, seas in sorted(full.items()):
    for sn, key in sorted(seas.items()):
        v = vals(key)
        hh = hashlib.md5(json.dumps(v).encode()).hexdigest()
        h2g[hh].append((g, sn, key, len(v)))
groups = sorted([v for v in h2g.values() if len(v) > 1], key=len, reverse=True)
out = []
out.append('genres>=8: %d' % len(full))
for grp in groups:
    gg = sorted(set(x[0] for x in grp))
    out.append(f'[{len(grp)} sets / {len(gg)} genres] genres={gg}')
    out.append('  ' + ', '.join(f'{g}/S{sn}({k},n={n})' for g, sn, k, n in grp))
open(r'C:\GensparkClaw\kujira-support\_s8.txt','w',encoding='utf-8').write('\n'.join(out))
print('groups:', len(groups))
# also: per-genre, are all seasons within genre identical to each other?
for g, seas in sorted(full.items()):
    hs = set(hashlib.md5(json.dumps(vals(k)).encode()).hexdigest() for k in seas.values())
    if len(hs) == 1:
        print('ALL-SEASONS-SAME:', g, len(seas))
