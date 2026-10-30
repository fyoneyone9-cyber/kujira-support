# シーズン間の outfit セット類似度チェック（個別シーン単位の流用率）
import re, collections, hashlib, json

s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()
sets = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json', encoding='utf-8'))

def scene_prompts(ref):
    v = sets.get(ref)
    if not v: return set()
    out = set()
    items = v.get('outfits', v) if isinstance(v, dict) else v
    if isinstance(items, list):
        for o in items:
            if isinstance(o, dict):
                p = o.get('value') or o.get('prompt') or ''
                if p: out.add(p.strip())
    return out

chars = []
for m in re.finditer(r"\{\s*id:\s*'(char_[^']+)'", s):
    block = s[m.start():m.start()+4000]
    rm = re.search(r'outfits_ref\s*:\s*"([^"]+)"', block)
    chars.append((m.group(1), rm.group(1) if rm else None))

def season_of(cid):
    m = re.search(r'_s(\d+)(?:_|$)', cid)
    return int(m.group(1)) if m else None
def genre_of(cid):
    m = re.match(r'char_(.+?)_s\d+(?:_|$)', cid)
    return m.group(1) if m else None

# genre -> season -> set of refs
g = collections.defaultdict(lambda: collections.defaultdict(set))
for cid, ref in chars:
    se, gr = season_of(cid), genre_of(cid)
    if se and gr and ref: g[gr][se].add(ref)

print('genre, seasonsペア流用率(>30%のみ表示)')
flag = 0
for gr, seasons in sorted(g.items()):
    if max(seasons) < 5: continue
    # union scene prompts per season
    sp = {}
    for se, refs in seasons.items():
        u = set()
        for r in refs: u |= scene_prompts(r)
        sp[se] = u
    ses = sorted(sp)
    for i in range(len(ses)):
        for j in range(i+1, len(ses)):
            a, b = sp[ses[i]], sp[ses[j]]
            if not a or not b: continue
            inter = len(a & b); denom = min(len(a), len(b))
            rate = inter/denom if denom else 0
            if rate > 0.3:
                flag += 1
                print(f'[FLAG] {gr} S{ses[i]}({len(a)}シーン) vs S{ses[j]}({len(b)}シーン): 共通{inter} ({rate:.0%})')
print()
print('flags:', flag)
# また、シーン数が極端に少ないシーズン（手抜き）も
print()
print('--- シーン数一覧（S5+ジャンル、シーン数5未満は要注意） ---')
for gr, seasons in sorted(g.items()):
    if max(seasons) < 5: continue
    counts = []
    for se in sorted(seasons):
        u = set()
        for r in seasons[se]: u |= scene_prompts(r)
        counts.append(f'S{se}:{len(u)}')
    print(gr, ' '.join(counts))
