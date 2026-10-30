import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 全rapeキャラをpush形式で抽出
pattern = re.compile(r"window\.CHAR_TEMPLATES\.female\.push\(\{([^;]{0,5000}?)\}\);", re.DOTALL)

chars = {}
for m in pattern.finditer(content):
    block = m.group(1)
    id_m = re.search(r"id:\s*['\"]([^'\"]+)['\"]", block)
    if not id_m: continue
    cid = id_m.group(1)
    if 'rape' not in cid: continue

    label_m = re.search(r"label:\s*['\"]([^'\"]+)['\"]", block)
    prompt_m = re.search(r"prompt:\s*['\"]([^'\"]{0,300})['\"]", block)
    outfits_ref_m = re.search(r"outfits_ref:\s*['\"]([^'\"]+)['\"]", block)
    # outfits数
    outfit_labels = re.findall(r'"label"\s*:\s*"([^"]+)"', block)

    chars[cid] = {
        'label': label_m.group(1) if label_m else '-',
        'prompt': prompt_m.group(1)[:120] if prompt_m else '-',
        'outfits_ref': outfits_ref_m.group(1) if outfits_ref_m else None,
        'outfit_count': len(outfit_labels),
    }

# グループ別に表示
groups = {
    'char_rape_jk_': 'JK',
    'char_rape_jd_': 'JD',
    'char_rape_chuugaku_': '中学',
    'char_rape_shougaku_': '小学',
    'char_rape_youjo_': '幼女',
    'char_rape_nyuuji_': '乳児',
    'char_rape_ff_': 'FF',
    'char_rape_legal_': '合法',
    'char_rape30_': '30日',
}

def get_group(cid):
    for prefix, name in groups.items():
        if cid.startswith(prefix):
            return name
    return 'その他'

from collections import defaultdict
by_group = defaultdict(list)
for cid, info in sorted(chars.items()):
    by_group[get_group(cid)].append((cid, info))

total = 0
issues = []
for grp in ['JK','JD','中学','小学','幼女','乳児','FF','合法','30日','その他']:
    members = by_group.get(grp, [])
    if not members: continue
    print(f'\n=== {grp} ({len(members)}体) ===')
    for cid, info in members:
        total += 1
        ref = f"ref:{info['outfits_ref']}" if info['outfits_ref'] else f"{info['outfit_count']}シーン"
        status = '✅' if (info['outfits_ref'] or info['outfit_count'] > 0) else '❌ outfitsなし'
        print(f"  {status} {cid}")
        print(f"     label: {info['label']}")
        print(f"     outfits: {ref}")
        if not info['outfits_ref'] and info['outfit_count'] == 0:
            issues.append(cid)

print(f'\n合計: {total}体')
if issues:
    print(f'\n❌ outfits未設定: {issues}')
else:
    print('\n✅ 全キャラoutfits設定済み')
