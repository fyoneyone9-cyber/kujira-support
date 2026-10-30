# 目的: CHAR_TEMPLATES内のキャラをジャンル×シーズンで集計し、outfits/scenesがコピー（同一値）のものを特定
import re, json, hashlib, collections
p = r'C:\AI\ComfyUI\dashboard.html'
s = open(p, encoding='utf-8', errors='ignore').read()

# push形式のキャラエントリを雑に抽出: id と outfits ブロック
ids = re.findall(r"window\.CHAR_TEMPLATES\.female\.push\(\{\s*id:\s*['\"]([^'\"]+)['\"]", s)
print('total push chars:', len(ids))

# シーズン付きIDのジャンル抽出
season_pat = re.compile(r'^(char_.+?)(?:_s([1-9]))?_([a-z0-9_]+)$')
genres = collections.Counter()
for i in ids:
    m = re.match(r'^char_([a-z0-9]+(?:_[a-z0-9]+)*?)(_s[1-9])?_[A-Za-z0-9]+$', i)
# simpler: find ids containing _s2_ .. _s5_
seas = collections.defaultdict(set)
for i in ids:
    m = re.search(r'_s([1-9])_', i)
    if m:
        g = i.split('_s'+m.group(1)+'_')[0]
        seas[g].add(int(m.group(1)))
print('genres with seasons:', len(seas))
for g, ss in sorted(seas.items()):
    print(g, sorted(ss))
