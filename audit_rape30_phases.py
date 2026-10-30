import sys, io, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 現在のフェーズキーワード（api_server側と同じ）
DRAG_KWS = [
    '引きずり','引き込','連れ込','dragged','grabbed','被われ',
    'abducted','kidnap','拉致','forced into','pulled into',
    'pushed into','being pushed','thrown into','shoved into',
    '押し込','押し倒','投げ込','引っ張','部屋に','連行',
]
BOUND_KWS = [
    '拘束','縛られ','tied','bound','restrained','wrists tied',
    'ankles bound','rope','手足','手首','ロープ','spread eagle',
]
STRIP_KWS = [
    '脱がされ','剥ぎ取','服を破','clothes torn','torn shirt',
    'skirt lifted','panties pulled','being stripped','forced undress',
]
AFTER_KWS = [
    '事後','after assault','lying limp','collapsed','curled up',
    '泣き崩','うずくまり','震えながら','終わった後','体を震',
    '床に倒れ','one arm covering chest','knees drawn up',
]
FEAR_KWS = [
    '帰り道','夜道','一人になる','footsteps','alone at night',
    'dark alley','followed','被われ前','気配','後ろから',
    '振り返','誰もいない','足音','孤独','街灯','暗い道',
]
GROOM_KWS = [
    '膝の上','お風呂','ないしょ','刷り込み','特別な遊び','パパだけのもの',
    '大好き','ふたりのひみつ','ふたりっきり','パパが好き','なついている',
    'grooming','lap sitting','bathing together','special secret','bedtime',
    'trusted adult','favorite place','just the two','our secret',
]
FILMING_KWS = [
    '撮影','記録','カメラ','証拠','写真','filming','recorded','camera','photograph',
    'being filmed','on camera','posed for','documentation',
]
CONDITIONING_KWS = [
    '感度開発','調教','バイブ','conditioning','trained','sensitivity','vibrator',
    '洗脳','刷り込','からだが慣れ','体が慣れ','週末は','ルーティン',
    'brainwash','mind control','weekly routine','conditioned response',
]
DISSOC_KWS = [
    '廃人','感情がなくなった','天井だけ見ていた','もう何も考えない','解離',
    '麻痺','空虚','虚ろ','dissociation','blank stare','empty eyes',
    'staring at ceiling','no emotion','mentally absent','thousand yard stare',
    'vacant expression','hollow','numb','detached',
]

def detect_phase(val):
    v = val.lower()
    if any(k in v for k in DRAG_KWS):       return 'drag'
    if any(k in v for k in BOUND_KWS):      return 'bound'
    if any(k in v for k in STRIP_KWS):      return 'strip'
    if any(k in v for k in AFTER_KWS):      return 'after'
    if any(k in v for k in FEAR_KWS):       return 'fear'
    if any(k in v for k in GROOM_KWS):      return 'groom'
    if any(k in v for k in FILMING_KWS):    return 'filming'
    if any(k in v for k in CONDITIONING_KWS): return 'conditioning'
    if any(k in v for k in DISSOC_KWS):     return 'dissoc'
    return 'GENERIC'

# rape30系キャラを抽出
pattern = re.compile(r"window\.CHAR_TEMPLATES\.female\.push\(\{([^;]{0,200000}?)\}\);", re.DOTALL)
unmatched = []
phase_counts = {}

for m in pattern.finditer(content):
    block = m.group(1)
    id_m = re.search(r"id:\s*['\"]([^'\"]+)['\"]", block)
    if not id_m: continue
    cid = id_m.group(1)
    if 'rape30' not in cid: continue

    # outfit labels と values を抽出
    outfits = re.findall(r'label:"([^"]+)",value:"([^"]{0,600})"', block)
    for label, val in outfits:
        phase = detect_phase(val + ' ' + label)
        if phase == 'GENERIC':
            unmatched.append((cid, label, val[:100]))
        phase_counts[phase] = phase_counts.get(phase, 0) + 1

print('=== フェーズ別カウント ===')
for p, n in sorted(phase_counts.items(), key=lambda x: -x[1]):
    print(f'  {p}: {n}件')

print(f'\n=== GENERIC（未分類）: {len(unmatched)}件 ===')
for cid, label, val in unmatched[:40]:
    print(f'  [{cid}] {label}')
    print(f'    value: {val}')
