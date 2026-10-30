# S5以上の書き下ろしチェック: 同一ジャンル内でシーズン間のprompt/outfits重複（コピー流用）を洗い出す
import re, collections, json

s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()

# push形式・配列形式両方からキャラオブジェクトを粗く抽出
# id と label と prompt らしき部分
char_blocks = []
for m in re.finditer(r"\{\s*id:\s*'(char_[^']+)'", s):
    start = m.start()
    cid = m.group(1)
    chunk = s[start:start+6000]
    lab = re.search(r"label:\s*'([^']*)'", chunk)
    pr = re.search(r"prompt:\s*'([^']*)'", chunk)
    char_blocks.append((cid, lab.group(1) if lab else '', pr.group(1) if pr else ''))

print('total chars:', len(char_blocks))

# シーズン番号抽出: _s5_ / _s5 末尾 / s5 内包
def season_of(cid):
    m = re.search(r'_s(\d+)(?:_|$)', cid)
    return int(m.group(1)) if m else None

def base_of(cid):
    return re.sub(r'_s\d+(?=_|$)', '', cid)

groups = collections.defaultdict(dict)  # base -> {season: (cid,label,prompt)}
for cid, lab, pr in char_blocks:
    se = season_of(cid)
    if se is None: continue
    groups[base_of(cid)][se] = (cid, lab, pr)

# S5以上を持つベースのみ
report = []
for base, seasons in groups.items():
    if max(seasons) < 5: continue
    # シーズン間でpromptが同一のものを検出
    dups = []
    items = sorted(seasons.items())
    for i in range(len(items)):
        for j in range(i+1, len(items)):
            s1, (c1, l1, p1) = items[i]
            s2, (c2, l2, p2) = items[j]
            if p1 and p1 == p2:
                dups.append((s1, s2, c1, c2))
    report.append((base, sorted(seasons), dups))

report.sort()
print('bases with S5+:', len(report))
print()
viol = 0
for base, se_list, dups in report:
    if dups:
        viol += 1
        print(f'[DUP] {base}  seasons={se_list}')
        for s1, s2, c1, c2 in dups:
            print(f'   S{s1}==S{s2}: {c1} / {c2}')
print()
print('violation bases:', viol)
# 欠番チェックも
print()
print('--- 欠番（S1..max に抜けあり） ---')
for base, se_list, dups in report:
    full = set(range(min(se_list), max(se_list)+1))
    missing = sorted(full - set(se_list))
    if missing:
        print(f'{base}: has {se_list} missing S{missing}')
