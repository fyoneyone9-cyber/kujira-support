import json, hashlib, collections, re
d = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json', encoding='utf-8'))
# S0273? keys
sk = [k for k in d if k.startswith('S0')]
print('S-keys:', len(sk), sk[:10])
if 'S0273' in d:
    a = d['S0273']
    print('S0273 items:', len(a))
    out = []
    for x in a[:6]:
        out.append(json.dumps(x, ensure_ascii=False)[:300])
    open(r'C:\GensparkClaw\kujira-support\_s4.txt','w',encoding='utf-8').write('\n\n'.join(out))
# check which S-sets are identical (copies)
h = {}
dups = collections.defaultdict(list)
for k in sk:
    hh = hashlib.md5(json.dumps(d[k], ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    dups[hh].append(k)
same = [v for v in dups.values() if len(v) > 1]
print('dup groups:', len(same))
for g in same[:30]:
    print(g)
