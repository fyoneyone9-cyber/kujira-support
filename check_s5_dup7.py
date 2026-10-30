# シーン0ジャンルの原因調査: refがjsonに存在するか / inline outfitsか
import re, json, collections, hashlib

s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()
sets = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json', encoding='utf-8'))

def season_of(cid):
    m = re.search(r'_s(\d+)(?:_|$)', cid)
    return int(m.group(1)) if m else None
def genre_of(cid):
    m = re.match(r'char_(.+?)_s\d+(?:_|$)', cid)
    return m.group(1) if m else None

def scene_prompts(ref):
    v = sets.get(ref)
    if not v: return None
    items = v.get('items', v.get('outfits', [])) if isinstance(v, dict) else v
    out = set()
    for o in items:
        if isinstance(o, dict):
            p = o.get('value') or o.get('prompt') or ''
            if p: out.add(p.strip())
    return out

# genre->season-> info
g = collections.defaultdict(lambda: collections.defaultdict(lambda: {'refs':set(),'missing':set(),'inline':0,'inline_hash':set(),'none':0}))
for m in re.finditer(r"\{\s*id:\s*'(char_[^']+)'", s):
    start = m.start(); cid = m.group(1)
    depth=0;i=start;end=min(len(s),start+80000)
    while i<end:
        c=s[i]
        if c=='{':depth+=1
        elif c=='}':
            depth-=1
            if depth==0:break
        i+=1
    block=s[start:i+1]
    se, gr = season_of(cid), genre_of(cid)
    if se is None or gr is None: continue
    d = g[gr][se]
    rm = re.search(r'outfits_ref\s*:\s*"([^"]+)"', block)
    if rm:
        ref=rm.group(1)
        d['refs'].add(ref)
        if ref not in sets: d['missing'].add(ref)
    else:
        om = re.search(r'outfits\s*:\s*\[', block)
        if om:
            j=om.end()-1;dd=0;k=j
            while k<len(block):
                if block[k]=='[':dd+=1
                elif block[k]==']':
                    dd-=1
                    if dd==0:break
                k+=1
            d['inline']+=1
            d['inline_hash'].add(hashlib.md5(block[j:k+1].encode()).hexdigest())
        else:
            d['none']+=1

for gr, seasons in sorted(g.items()):
    if max(seasons)<5: continue
    probs=[]
    # inline hash重複(シーズン間)
    usage=collections.defaultdict(set)
    for se,d in seasons.items():
        for h in d['inline_hash']: usage[h].add(se)
        if d['missing']: probs.append(f"S{se}: ref欠落 {sorted(d['missing'])}")
        if d['none']: probs.append(f"S{se}: outfits未定義キャラ{d['none']}体")
    for h,ss in usage.items():
        if len(ss)>1: probs.append(f"inline outfits同一コピー: S{sorted(ss)}")
    if probs:
        print(f'[NG] {gr} seasons={sorted(seasons)}')
        for p in probs: print('   ',p)
