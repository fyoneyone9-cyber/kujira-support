import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# RAPE_COMP_V2と同じキーワードセット
PHASES = [
    ('drag', ['引きずり','引き込','連れ込','拉致','連行','押し込','押し倒','投げ込','引っ張','部屋に','監禁部屋','dragged','grabbed','abducted','kidnap','forced into','pulled into','pushed into','being pushed','thrown into','shoved into','locked in','chain collar','首にチェーン','collar clicking','chain clicked','collar being locked','チェーンを付']),
    ('bound', ['拘束','縛られ','手足','手首','ロープ','足首','四肢','tied','bound','restrained','rope','cuffed','chained','wrists tied','ankles bound','spread eagle','arms above','arms raised','bound to','fixed in place','cannot move','immobilized','helpless position']),
    ('strip', ['脱がされ','剥ぎ取','服を破','服を引き','スカートをめくられ','clothes torn','torn shirt','skirt lifted','panties pulled','being stripped','forced undress','clothes ripped','shirt torn','bra removed','clothes being removed','undressing her','exposed skin','nakedness revealed']),
    ('pregnant', ['妊娠','お腹','臨月','陣痛','出産','胎動','母乳','授乳','産後','破水','いきむ','赤ちゃん','newborn','pregnant','pregnancy','belly','baby','labor pain','contractions','giving birth','postpartum','breast milk','breastfeeding','belly bump','round belly','pregnant belly']),
    ('after', ['事後','終わった後','放置','完全に疲弊','傷だらけ','after assault','lying limp','collapsed','curled up','泣き崩','うずくまり','震えながら','体を震','床に倒れ','one arm covering chest','knees drawn up','left alone','abandoned after','sobbing alone','broken','lying on floor','lying face down','arms limp']),
    ('fear', ['帰り道','夜道','追跡','後をつけ','足音','一人に','気配','振り返','誰もいない','暗い道','街灯','孤独','footsteps','walking faster','turning to check','alone at night','pursued','being followed','feeling watched','growing uncertain','dark alley','empty street','no one around','shadowed','night road']),
    ('groom', ['膝の上','お風呂','ないしょ','パパだけのもの','特別な遊び','大好き','ふたりのひみつ','なついている','パパが好き','lap sitting','bathing together','special secret','bedtime','trusted adult','our secret','just the two','gentle touch','grooming']),
    ('filming', ['撮影','記録','カメラ','証拠','写真','カメラを向け','filming','recorded','camera','photograph','on camera','being filmed','posed for','documentation','video','taking photos','snapshot','evidence photo']),
    ('conditioning', ['感度開発','調教','バイブ','週末は','ルーティン','体が慣れ','conditioning','trained','sensitivity','vibrator','brainwash','mind control','weekly routine','conditioned response','behavioral conditioning','trained to','obedient','submissive posture']),
    ('dissoc', ['廃人','感情がなくなった','天井だけ見ていた','もう何も考えない','解離','麻痺','空虚','虚ろ','呆然','完全に疲弊','床で呆然','vacant open eyes','arms limp','head turned sideways','dissociation','blank stare','empty eyes','staring at ceiling','no emotion','mentally absent','thousand yard stare','vacant expression','hollow','numb','detached','lying face down on floor','utterly exhausted']),
    ('pov', ['pov','first person','looking up at','upward gaze','見上げ','上から','加害者視点','俯瞰','監視','predator pov','from above perspective','looking down at her','voyeur','watching from','observed']),
    ('touch', ['触れ','体を触','手が触','なでる','撫で','肌に触','touching','groping','hand on','caressing','feeling up','first touch','body contact','unwanted touch']),
]

def detect(val, label):
    t = (val + ' ' + label).lower()
    for phase, kws in PHASES:
        if any(k in t for k in kws):
            return phase
    return 'GENERIC'

pattern = re.compile(r"window\.CHAR_TEMPLATES\.female\.push\(\{([^;]{0,200000}?)\}\);", re.DOTALL)
counts = {}
generic_samples = []

for m in pattern.finditer(content):
    block = m.group(1)
    id_m = re.search(r"id:\s*['\"]([^'\"]+)['\"]", block)
    if not id_m: continue
    cid = id_m.group(1)
    if 'rape' not in cid: continue

    for label, val in re.findall(r'label:"([^"]+)",value:"([^"]{0,600})"', block):
        p = detect(val, label)
        counts[p] = counts.get(p, 0) + 1
        if p == 'GENERIC' and len(generic_samples) < 15:
            generic_samples.append((cid, label, val[:80]))

print('=== RAPE_COMP_V2 フェーズ別カウント ===')
total = sum(counts.values())
for p, n in sorted(counts.items(), key=lambda x: -x[1]):
    print(f'  {p:15s}: {n:3d}件 ({n*100//total}%)')
print(f'  合計: {total}件')

print(f'\n=== GENERIC残り: {len(generic_samples)}件サンプル ===')
for cid, label, val in generic_samples:
    print(f'  [{label}] {val}')
