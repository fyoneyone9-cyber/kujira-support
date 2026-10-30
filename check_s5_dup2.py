# S5+ジャンル: シーズン間で outfits(シーン書き下ろし) が同一流用かを判定
import re, collections, json, hashlib

s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()

# 各キャラオブジェクト全体を括弧バランスで抽出
results = []
for m in re.finditer(r"\{\s*id:\s*'(char_[^']+)'", s):
    start = m.start(); cid = m.group(1)
    depth = 0; i = start
    end = min(len(s), start + 60000)
    while i < end:
        c = s[i]
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0: break
        i += 1
    block = s[start:i+1]
    om = re.search(r'outfits\s*:\s*\[', block)
    outf = ''
    if om:
        j = om.end()-1; d=0; k=j
        while k < len(block):
            if block[k]=='[': d+=1
            elif block[k]==']':
                d-=1
                if d==0: break
            k+=1
        outf = block[j:k+1]
    pr = re.search(r"prompt:\s*'([^']*)'", block)
    results.append((cid, hashlib.md5(outf.encode()).hexdigest() if outf else None,
                    len(outf), pr.group(1)[:60] if pr else ''))

def season_of(cid):
    m = re.search(r'_s(\d+)(?:_|$)', cid)
    return int(m.group(1)) if m else None
def base_of(cid):
    return re.sub(r'_s\d+(?=_|$)', '', cid)

groups = collections.defaultdict(dict)
for cid, h, ln, pr in results:
    se = season_of(cid)
    if se is None: continue
    # 重複ID対策: 後勝ち(JSと同じ)
    groups[base_of(cid)][se] = (cid, h, ln)

viol = {}
for base, seasons in groups.items():
    mx = max(seasons)
    if mx < 5: continue
    # S5以上のシーズンについて、他シーズンとoutfitsハッシュ一致があるか
    byhash = collections.defaultdict(list)
    for se, (cid, h, ln) in seasons.items():
        if h: byhash[h].append(se)
    dup_sets = [sorted(v) for v in byhash.values() if len(v) > 1]
    no_outf = sorted(se for se,(cid,h,ln) in seasons.items() if not h)
    if dup_sets or no_outf:
        viol[base] = (sorted(seasons), dup_sets, no_outf)

print('S5+ ベース数:', sum(1 for b,se in groups.items() if max(se)>=5))
print('違反ベース数:', len(viol))
print()
for base in sorted(viol):
    se_list, dup_sets, no_outf = viol[base]
    msg = []
    for d in dup_sets: msg.append('同一outfits: S' + '=S'.join(map(str,d)))
    if no_outf: msg.append('outfitsなし: S' + ',S'.join(map(str,no_outf)))
    print(f'{base} seasons={se_list}')
    for mm in msg: print('   ', mm)
