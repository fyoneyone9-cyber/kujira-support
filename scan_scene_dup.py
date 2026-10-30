# 入力: dashboard.html / 出力: tifa/aerithキャラのジャンル別シーン重複状況
# 目的: 「シーンvalueがコピーのまま」の19ジャンルを特定する
import re, sys, json, collections
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p = r'C:\AI\ComfyUI\dashboard.html'
s = open(p, encoding='utf-8').read()

def extract_obj(start):
    # start = index of "push({" の '{' 相当。idマッチ位置から前後にscenesを探す
    pass

# キャラごとに id位置から次のid位置までを1ブロックとみなし、scenes内のvalueを収集
ids = [(m.group(1), m.start()) for m in re.finditer(r"id:\s*'([^']*(?:tifa|aerith)[^']*)'", s)]
genre = collections.defaultdict(dict)  # genre -> {charid: [values]}
for i,(cid,pos) in enumerate(ids):
    end = ids[i+1][1] if i+1 < len(ids) else pos+60000
    block = s[pos:end]
    # scenes: [ {label:'..', value:'..'}, ... ]
    mm = re.search(r"scenes\s*:\s*\[(.*?)\]", block, re.S)
    scenes = []
    if mm:
        for sm in re.finditer(r"label:\s*'((?:[^'\\]|\\.)*)'\s*,\s*value:\s*'((?:[^'\\]|\\.)*)'", mm.group(1)):
            scenes.append((sm.group(1), sm.group(2)))
    g = re.sub(r'_s\d+_', '_SX_', cid)
    g = re.sub(r'_(tifa|aerith)(_v2)?$', '', g)
    genre[g][cid] = scenes

# ジャンルごと: シーン総数とユニークvalue数
rows=[]
for g, chars in sorted(genre.items()):
    allv=[]
    n=0
    for cid, sc in chars.items():
        n += len(sc)
        allv += [v for _,v in sc]
    uniq = len(set(allv))
    if n>0:
        rows.append((g, len(chars), n, uniq))
for g,nc,n,u in rows:
    flag = ' <<< COPY' if n>0 and u*3<=n else ''
    print(f'{g} | chars={nc} scenes={n} uniq={u}{flag}')
