# S5+ジャンル: シーズン間で outfits_ref または インラインoutfits が使い回されていないか
# 違反定義: 同一ジャンル(プレフィックス)内で、異なるシーズンが同じ outfits_ref / 同一outfitsハッシュを共有
import re, collections, hashlib

s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()

chars = []  # (cid, ref or hash)
for m in re.finditer(r"\{\s*id:\s*'(char_[^']+)'", s):
    start = m.start(); cid = m.group(1)
    depth = 0; i = start
    end = min(len(s), start + 80000)
    while i < end:
        c = s[i]
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0: break
        i += 1
    block = s[start:i+1]
    rm = re.search(r'outfits_ref\s*:\s*"([^"]+)"', block)
    if rm:
        key = 'REF:' + rm.group(1)
    else:
        om = re.search(r'outfits\s*:\s*\[', block)
        if om:
            j = om.end()-1; d=0; k=j
            while k < len(block):
                if block[k]=='[': d+=1
                elif block[k]==']':
                    d-=1
                    if d==0: break
                k+=1
            key = 'HASH:' + hashlib.md5(block[j:k+1].encode()).hexdigest()
        else:
            key = None
    chars.append((cid, key))

def season_of(cid):
    m = re.search(r'_s(\d+)(?:_|$)', cid)
    return int(m.group(1)) if m else None

def genre_of(cid):
    # char_<genre>_sN_<name> -> genre
    m = re.match(r'char_(.+?)_s\d+(?:_|$)', cid)
    return m.group(1) if m else None

# genre -> season -> set of outfit keys
g = collections.defaultdict(lambda: collections.defaultdict(set))
for cid, key in chars:
    se = season_of(cid); gr = genre_of(cid)
    if se is None or gr is None: continue
    g[gr][se].add(key)

print('ジャンル総数(シーズン制):', len(g))
viol = []
for gr, seasons in sorted(g.items()):
    if max(seasons) < 5: continue
    # key -> which seasons use it
    usage = collections.defaultdict(set)
    for se, keys in seasons.items():
        for k in keys:
            if k: usage[k].add(se)
    shared = {k: sorted(v) for k, v in usage.items() if len(v) > 1}
    none_seasons = sorted(se for se, keys in seasons.items() if keys == {None})
    if shared or none_seasons:
        viol.append((gr, sorted(seasons), shared, none_seasons))

print('S5+ ジャンル数:', sum(1 for gr,se in g.items() if max(se)>=5))
print('違反ジャンル数:', len(viol))
print()
for gr, se_list, shared, none_seasons in viol:
    print(f'[NG] {gr}  seasons={se_list}')
    for k, ss in sorted(shared.items()):
        print(f'    使い回し {k[:40]} -> S{ss}')
    if none_seasons:
        print(f'    outfits未定義: S{none_seasons}')
print()
print('--- OK（全シーズン独立書き下ろし） ---')
for gr, seasons in sorted(g.items()):
    if max(seasons) < 5: continue
    if not any(v[0]==gr for v in viol):
        print('OK', gr, sorted(seasons))
