# tifa/aerithキャラの outfits_ref を集め、ジャンル内/間でセット内容が同一コピーのものを検出
import re,sys,json,hashlib,collections
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
s=open(r'C:\AI\ComfyUI\dashboard.html',encoding='utf-8').read()
sets=json.load(open(r'C:\AI\ComfyUI\outfit_sets.json',encoding='utf-8'))

def h(ref):
    a=sets.get(ref)
    if not a: return None
    return hashlib.md5(json.dumps(a,ensure_ascii=False,sort_keys=True).encode()).hexdigest()[:10]

rows=[]
for m in re.finditer(r"id:\s*'([^']*(?:tifa|aerith)[^']*)'[^\n]*?outfits_ref:\s*\"(S\d+)\"",s):
    rows.append((m.group(1),m.group(2)))
print('tifa/aerith chars with outfits_ref:',len(rows))
# group by genre
genre=collections.defaultdict(list)
for cid,ref in rows:
    g=re.sub(r'_s\d+(_ff)?_(tifa|aerith)$','',cid)
    g=re.sub(r'_(tifa|aerith)$','',g)
    genre[g].append((cid,ref))
hashmap=collections.defaultdict(list)
for g,lst in sorted(genre.items()):
    refs=sorted(set(r for _,r in lst))
    hs=[h(r) for r in refs]
    uniq=len(set(hs))
    print(f'{g}: refs={len(refs)} uniq_content={uniq} refs={refs[:12]}')
    for r,hh in zip(refs,hs):
        hashmap[hh].append((g,r))
print()
print('== identical content groups (copies) ==')
for hh,lst in hashmap.items():
    if len(lst)>1:
        print(hh, lst)
