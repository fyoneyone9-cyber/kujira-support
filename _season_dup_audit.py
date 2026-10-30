# -*- coding: utf-8 -*-
# シーズン系列（S1〜S10等）でキャラプロンプト/outfitsがどれだけ使い回しかを監査
import io, re, sys, collections, hashlib
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

t = io.open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()

# キャラID全部と、そのオブジェクト本文のハッシュを取る（pushブロック単位は困難なので idごとに近傍を使う）
# 方法: id:'char_xxx' の出現位置から次の id:'char_ までを1キャラ分とみなす
ids = [(m.group(1), m.start()) for m in re.finditer(r"id:\s*'(char_[a-z0-9_]+)'", t)]
print('total char ids:', len(ids))

# シーズン系列を抽出: char_<base>_s<N>_<rest> または char_<base>_sN...
series = collections.defaultdict(lambda: collections.defaultdict(list))  # base -> season -> [(id,start,end)]
for idx, (cid, pos) in enumerate(ids):
    end = ids[idx+1][1] if idx+1 < len(ids) else pos + 20000
    m = re.match(r'char_([a-z0-9_]+?)_s(\d+)_(.+)', cid)
    if m:
        base, sn, rest = m.group(1), int(m.group(2)), m.group(3)
        series[base][sn].append((rest, cid, pos, min(end, pos+20000)))

def body_sig(pos, end):
    # outfitsのprompt/valueテキストだけ抽出して正規化ハッシュ
    seg = t[pos:end]
    prompts = re.findall(r"(?:prompt|value)\s*:\s*'([^']*)'", seg) + re.findall(r'(?:prompt|value)\s*:\s*"([^"]*)"', seg)
    joined = '|'.join(prompts)
    return hashlib.md5(joined.encode('utf-8','ignore')).hexdigest(), len(prompts), joined

results = []
for base, seasons in sorted(series.items()):
    if len(seasons) < 2: continue
    # 各シーズンで同じrest名のキャラのプロンプト署名を比較
    # シーズン間で共通するrest名
    restsets = {sn: {r[0] for r in lst} for sn, lst in seasons.items()}
    common = set.intersection(*restsets.values()) if restsets else set()
    if not common: 
        results.append((base, len(seasons), 0, 0, 'rest名が季節間で不一致'))
        continue
    same = 0; diff = 0
    for rest in common:
        sigs = set()
        for sn, lst in seasons.items():
            for r, cid, p, e in lst:
                if r == rest:
                    sigs.add(body_sig(p, e)[0])
        if len(sigs) == 1: same += 1
        else: diff += 1
    results.append((base, len(seasons), same, diff, ''))

print()
print('=== シーズン系列のプロンプト使い回し状況 ===')
print('(same=全シーズンで完全同一プロンプトのキャラ数 / diff=シーズンごとに異なるキャラ数)')
print()
results.sort(key=lambda x: -(x[2]/(x[2]+x[3]) if (x[2]+x[3]) else 0))
for base, ns, same, diff, note in results:
    tot = same + diff
    pct = (same/tot*100) if tot else 0
    print(f'{base:22s} シーズン数:{ns:2d}  共通キャラ:{tot:3d}  完全使い回し:{same:3d} ({pct:5.1f}%)  {note}')
