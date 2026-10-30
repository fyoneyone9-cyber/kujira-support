# 最終チェック: S5+ジャンル全件、シーズン間のシーン(value)流用率
import re, json, collections
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()
sets = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json', encoding='utf-8'))

def items_of(ref):
    v = sets.get(ref)
    if v is None: return None
    items = v.get('items', v.get('outfits', [])) if isinstance(v, dict) else v
    return set((o.get('value') or o.get('prompt') or '').strip() for o in items if isinstance(o, dict))

def season_of(cid):
    m = re.search(r'_s(\d+)(?:_|$)', cid)
    return int(m.group(1)) if m else None
def genre_of(cid):
    m = re.match(r'char_(.+?)_s\d+(?:_|$)', cid)
    return m.group(1) if m else None

g = collections.defaultdict(lambda: collections.defaultdict(set))  # genre->season->refs
noref = collections.defaultdict(lambda: collections.defaultdict(int))
for m in re.finditer(r"id:\s*'(char_[^']+)'", s):
    cid = m.group(1)
    se, gr = season_of(cid), genre_of(cid)
    if se is None or gr is None: continue
    block = s[m.start():m.start()+5000]
    rm = re.search(r'outfits_ref\s*:\s*"([^"]+)"', block)
    if rm: g[gr][se].add(rm.group(1))
    else: noref[gr][se] += 1

print('=== S5+ジャンル検査結果 ===')
ngs = 0
for gr, seasons in sorted(g.items()):
    allse = set(seasons) | set(noref.get(gr, {}))
    if not allse or max(allse) < 5: continue
    probs = []
    sp = {}
    for se, refs in seasons.items():
        u = set()
        for r in refs:
            it = items_of(r)
            if it is None: probs.append(f'S{se}: ref {r} がoutfit_sets.jsonに無い')
            else: u |= it
        sp[se] = u
    for se, cnt in noref.get(gr, {}).items():
        probs.append(f'S{se}: outfits_refなしキャラ {cnt}体')
    ses = sorted(sp)
    for i in range(len(ses)):
        for j in range(i+1, len(ses)):
            a, b = sp[ses[i]], sp[ses[j]]
            if not a or not b: continue
            inter = len(a & b); rate = inter / min(len(a), len(b))
            if rate > 0.2:
                probs.append(f'S{ses[i]}とS{ses[j]}: シーン{inter}件流用 ({rate:.0%})')
    for se in ses:
        if len(sp[se]) < 10:
            probs.append(f'S{se}: シーン数わずか{len(sp[se])}件')
    if probs:
        ngs += 1
        print(f'[NG] {gr} seasons={sorted(allse)}')
        for p in probs: print('   ', p)
print()
print(f'S5+ジャンル {sum(1 for gr,se in g.items() if se and max(se)>=5)}件中 違反 {ngs}件')
