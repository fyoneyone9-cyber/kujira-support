# outfit_sets.json のセット中身レベルで、S5+ジャンルのシーズン間コピーを検出
import re, collections, hashlib, json

s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()
sets = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json', encoding='utf-8'))
print('sets:', len(sets))

def set_hash(ref):
    v = sets.get(ref)
    if v is None: return None
    return hashlib.md5(json.dumps(v, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

chars = []
for m in re.finditer(r"\{\s*id:\s*'(char_[^']+)'", s):
    start = m.start(); cid = m.group(1)
    block = s[start:start+4000]
    rm = re.search(r'outfits_ref\s*:\s*"([^"]+)"', block)
    chars.append((cid, rm.group(1) if rm else None))

def season_of(cid):
    m = re.search(r'_s(\d+)(?:_|$)', cid)
    return int(m.group(1)) if m else None
def genre_of(cid):
    m = re.match(r'char_(.+?)_s\d+(?:_|$)', cid)
    return m.group(1) if m else None

g = collections.defaultdict(lambda: collections.defaultdict(set))  # genre->season->set of content-hash
refmap = collections.defaultdict(lambda: collections.defaultdict(set))
for cid, ref in chars:
    se = season_of(cid); gr = genre_of(cid)
    if se is None or gr is None or not ref: continue
    h = set_hash(ref)
    g[gr][se].add(h)
    refmap[gr][se].add(ref)

viol = 0
for gr, seasons in sorted(g.items()):
    if max(seasons) < 5: continue
    usage = collections.defaultdict(set)
    for se, hs in seasons.items():
        for h in hs:
            usage[h].add(se)
    shared = {h: sorted(v) for h, v in usage.items() if len(v) > 1 and h}
    missing = sorted(se for se, hs in seasons.items() if None in hs)
    if shared or missing:
        viol += 1
        print(f'[NG] {gr} seasons={sorted(seasons)}')
        for h, ss in shared.items():
            refs = set()
            for se in ss: refs |= refmap[gr][se]
            print(f'    中身同一コピー: S{ss} refs={sorted(refs)}')
        if missing:
            print(f'    ref未定義(jsonに無い): S{missing}')
print()
print('違反ジャンル数:', viol, '/', sum(1 for gr,se in g.items() if max(se)>=5))
