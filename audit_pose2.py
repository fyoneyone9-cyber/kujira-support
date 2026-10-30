import sys, io, re, ast
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ファイルから POSE_TABLE を実際に抽出
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

in_table = False
table_src = []
for i, l in enumerate(lines):
    if '_POSE_TABLE = [' in l:
        in_table = True
    if in_table:
        table_src.append(l)
        if l.strip() == ']':
            break

# キーワードリストを正規表現で抽出
POSE_TABLE = []
for i, line in enumerate(table_src):
    m = re.match(r'\s*\("(\w+)"\s*,\s*(\d+)\s*,\s*(\[.*)', ''.join(table_src).split('\n')[i] if False else line)
    pass

# シンプル方法: 全キーワードを名前→キーワードでフラット化
# テキスト全体から ("name", N, [...], [...]) を解析
full = ''.join(table_src)
entries = re.findall(r'\("(\w+)"\s*,\s*(\d+)\s*,\s*(\[.*?\])\s*,\s*(\[.*?\])\s*\)', full, re.DOTALL)

POSE_TABLE_PARSED = []
for name, prio, exact_s, ambig_s in entries:
    try:
        exact = ast.literal_eval(exact_s.replace('\n','').replace('  ',' '))
    except:
        exact = []
    try:
        ambig = ast.literal_eval(ambig_s.replace('\n','').replace('  ',' '))
    except:
        ambig = []
    POSE_TABLE_PARSED.append((name, int(prio), exact, ambig))

# キーワード確認
print('=== POSE_TABLE 実ファイルから読んだキーワード一覧 ===')
for name, prio, exact, ambig in POSE_TABLE_PARSED:
    print(f'  [{prio:2d}] {name}: {len(exact)}固有, {len(ambig)}曖昧')
    for kw in exact:
        print(f'        exact: {kw}')
    for kw in ambig:
        print(f'        ambig: {kw}')

print()

def detect_pose_from_file(val, has_sex_act=True):
    low = val.lower()
    for name, prio, exact, ambig in sorted(POSE_TABLE_PARSED, key=lambda x: x[1]):
        for kw in exact:
            if kw in low:
                return name, kw, prio, 'exact'
        if has_sex_act:
            for kw in ambig:
                if kw in low:
                    return name, kw, prio, 'ambig'
    return None, None, None, None

# 誤発火テスト
print('=== 誤発火テスト（ファイル実定義） ===')
tests = [
    ("on all fours, crawling on floor, no sex, fully clothed", None, False, "四つん這い非性行為"),
    ("on all fours, doggy style, penetration", "doggy", True, "四つん這い+性行為→doggy"),
    ("multiple men watching, not sex", None, True, "複数男性見学のみ"),
    ("gangbang, multiple cocks, group rape", "gangbang", True, "gangbang正常"),
    ("large creampie, semen overflowing", "creampie_after", True, "大量中出し事後"),
    ("semen leaking from vagina, dripping down thigh", "creampie_after", True, "中出し漏れ事後"),
    ("cum dripping from vagina, large creampie inside", "creampie_after", True, "cum dripping from vagina"),
    ("cum on face, facial cumshot, kneeling", "bukkake", True, "顔射bukakke"),
    ("cum splattered all over body", "bukkake", True, "全身ぶっかけ"),
    ("gagging, choking, drug, dazed", "gagged", True, "薬物gagging→gagged誤発火?"),
    ("deepthroat, gagging on penis", "fellatio", True, "deepthroat→fellatio優先"),
    ("rear penetration, prone position on bed", "pronebone", True, "pronebone正常"),
    ("leather collar fastened, leash pulled, nude kneeling", "bondage", True, "首輪bondage"),
    ("anal spread, anus visible, no penetration", None, False, "肛門露出のみ(非性行為)"),
    ("anal spread, finger penetration, anus", "fingering", True, "肛門指姦"),
    ("semen splattered on face, cum on face", "bukkake", True, "顔への精液→bukakke"),
]

ok = err = 0
for val, expected, has_sex, desc in tests:
    pose, kw, prio, match_type = detect_pose_from_file(val, has_sex_act=has_sex)
    result = "✅" if pose == expected else "❌"
    if pose == expected:
        ok += 1
    else:
        err += 1
    print(f'{result} {desc}')
    print(f'   検出: {pose}(kw="{kw}", prio={prio}, {match_type}) | 期待: {expected}')

print(f'\n結果: {ok}✅ / {err}❌')
print()
print('=== キーワード重複チェック ===')
all_kws = {}
dup = 0
for name, prio, exact, ambig in POSE_TABLE_PARSED:
    for kw in exact:
        if kw in all_kws:
            print(f'❌ 重複: "{kw}" → {all_kws[kw]} AND {name}(prio={prio})')
            dup += 1
        else:
            all_kws[kw] = f'{name}(prio={prio})'
if dup == 0:
    print('重複なし ✅')
