# 目的: 「コピーしかない」19ジャンルを特定する。
# 方法: dashboardのoutfits_ref("Sxxxx")を持つ季節付きキャラからジャンル→シーズン→Sキーをマップし、
#       outfit_sets.jsonのvalue本文（ラベル除く）がジャンル間/シーズン間でどれだけ重複しているか計測。
import re, json, collections, hashlib
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()
d = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json', encoding='utf-8'))

# char id -> outfits_ref
pairs = re.findall(r"id:\s*['\"](char_[^'\"]+)['\"][^}]*?outfits_ref\s*:\s*['\"]([^'\"]+)['\"]", s)
gmap = collections.defaultdict(dict)  # genre -> season -> set of refs
for cid, ref in pairs:
    m = re.search(r'^char_([a-z0-9_]+?)_s([0-9])_', cid)
    if m:
        gmap[m.group(1)].setdefault(int(m.group(2)), set()).add(ref)
    else:
        m2 = re.match(r'^char_([a-z0-9_]+?)_(youchien|shougaku|chuugaku|jk|tifa|aerith|jd|ol)', cid)
        if m2:
            gmap[m2.group(1)].setdefault(1, set()).add(ref)

out = []
for g in sorted(gmap):
    seasons = gmap[g]
    out.append(f'{g}: ' + ', '.join(f'S{k}={sorted(v)}' for k, v in sorted(seasons.items())))
open(r'C:\GensparkClaw\kujira-support\_s5.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('genres:', len(gmap))

# value-body duplication across all S-sets
valhash = collections.defaultdict(list)
for k, arr in d.items():
    if not isinstance(arr, list):
        continue
    vals = tuple(x.get('value', '') for x in arr if isinstance(x, dict))
    valhash[hashlib.md5(json.dumps(vals).encode()).hexdigest()].append(k)
dupsets = [v for v in valhash.values() if len(v) > 1]
print('identical-value set groups:', len(dupsets))
for g in dupsets[:40]:
    print(g)
