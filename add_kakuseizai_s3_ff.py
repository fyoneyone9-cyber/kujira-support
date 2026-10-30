"""
覚醒剤S3 ティファ・エアリス
- S1,S2と完全新規・重複なし
- S上がるごとに過激（S3=最高段階）
- S3コンセプト: 完全な支配・複数・廃人化の極限・道具として消費される段階
- ティファ/エアリスそれぞれのキャラ特性を活かした描写
"""
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# =========================================================
# S3共通プロンプトベース（ティファ用・エアリス用それぞれ定義）
# =========================================================

TIFA_BASE = "(Tifa Lockhart:1.5),(Final Fantasy VII:1.35),(black hair long:1.3),(red eyes:1.2),(large breasts:1.6),(athletic body:1.4),(black mini dress:1.2),(leather suspenders:1.2),(white gloves partially:1.1)"
AERITH_BASE = "(Aerith Gainsborough:1.5),(Final Fantasy VII:1.35),(light brown hair ponytail pink ribbon:1.3),(green eyes:1.2),(medium breasts:1.35),(slender body:1.3),(pink dress:1.2),(red jacket partially off:1.1)"

COMMON_QUALITY = "(masterpiece:1.2),(best quality:1.2),(ultra detailed:1.3),(photorealistic:1.5),(1girl:1.5),(solo:1.5),(anatomically correct:1.5)"

# =========================================================
# S3 30シーン定義
# S1: 薬物使用の初期〜性行為開始
# S2: 強制・暴力・人形化・廃人化
# S3: 多人数・完全な道具化・極限・廃人後も使われる
# =========================================================

S3_SCENES = [
    # 00-04: 薬物投与・最初の崩壊（S1/S2より強制的・残虐）
    {
        "label": "00「静脈直撃」首の静脈に直接注射される",
        "scene": "syringe injected into neck vein,restrained arms,extreme close-up neck injection,terror in eyes,beginning to lose consciousness,medical restraints,clinical setting perverted,pupils dilating rapidly,first wave of forced drugging",
        "pose": "upper body,close-up,from front",
        "expr": "(terror expression:1.5),(wide open eyes:1.4),(tears streaming:1.3)",
        "clothes": "clothes on,restrained",
    },
    {
        "label": "01「二重摂取」一度では足りないと二本目を打たれる",
        "scene": "two syringes,second injection while first still active,overpowering drug effect,body trembling violently,foam at mouth beginning,eyes rolling back halfway,captive sitting position,bruised arm from multiple injections,crying unable to resist",
        "pose": "upper body,from front",
        "expr": "(overwhelmed expression:1.5),(half-rolled eyes:1.4),(trembling lips:1.3)",
        "clothes": "clothes disheveled",
    },
    {
        "label": "02「過剰投与」致死量に近い量を体に流し込まれる",
        "scene": "massive drug overdose,entire body convulsing,veins visible on skin,extreme pupils dilation,barely conscious,limp body held up by others,drool running freely,heart racing visibly,survival in question",
        "pose": "full body,lying down,from above",
        "expr": "(barely conscious:1.6),(eyes rolled back 90%:1.5),(drooling heavily:1.4)",
        "clothes": "clothes barely on,disarray",
    },
    {
        "label": "03「脳神経焼却」快楽中枢が焼き切れる感覚",
        "scene": "neurological overload,body arching backwards violently,spine visible through tension,eyes completely rolled back showing whites,screaming silently,fingers clawing air,drug-induced seizure,mind completely destroyed by pleasure overload",
        "pose": "full body,arching back,from side",
        "expr": "(ahegao extreme:1.8),(completely rolled back eyes:1.7),(mouth wide open silent scream:1.5)",
        "clothes": "clothes torn apart",
    },
    {
        "label": "04「支配確立」意識が完全に薬に支配される",
        "scene": "completely drugged glazed eyes,sitting obediently,blank expression of total submission,following orders without thought,leash around neck,collar,completely controlled,vacant stare,waiting for next command",
        "pose": "upper body,sitting,from front",
        "expr": "(completely blank expression:1.6),(empty eyes:1.5),(vacant obedient look:1.4)",
        "clothes": "stripped to underwear,collar",
    },
    # 05-09: 複数人・輪姦
    {
        "label": "05「初めての輪姦」複数人に同時に犯される",
        "scene": "gangbang,multiple men surrounding,penetrated from behind while forced oral,tears streaming,overwhelming stimulation from multiple directions,body completely used as object,no escape,ahegao beginning,multiple hands groping",
        "pose": "full body,on all fours,from side",
        "expr": "(overwhelmed ahegao:1.6),(forced pleasure expression:1.5),(tears:1.4)",
        "clothes": "completely naked,collar",
    },
    {
        "label": "06「三穴同時」全ての穴を埋め尽くされる",
        "scene": "triple penetration,anal vaginal oral simultaneous,complete bodily violation,eyes showing only whites,tongue being forced,body used from all angles,extreme stimulation overload,consciousness barely retained,complete ahegao",
        "pose": "full body,from side",
        "expr": "(extreme ahegao:1.8),(eyes completely white:1.7),(drooling saliva strings:1.5)",
        "clothes": "naked",
    },
    {
        "label": "07「列を成す」順番待ちで使われる",
        "scene": "multiple men waiting in line,being used one after another without rest,exhausted but unable to stop,drugs keeping conscious,body covered in marks,previous fluids covering body,mechanical repetition,no longer human treatment",
        "pose": "upper body,from front,exhausted",
        "expr": "(completely broken expression:1.6),(mechanical ahegao:1.5),(empty eyes:1.4)",
        "clothes": "naked,cum covered",
    },
    {
        "label": "08「拘束輪姦」完全に縛られた状態で犯される",
        "scene": "bondage restraints,rope bound wrists ankles,spread eagle position,completely helpless,multiple attackers,unable to resist or move,face down position,forced from behind,face pressed into surface",
        "pose": "full body,spread eagle,from behind",
        "expr": "(helpless expression:1.5),(pain and forced pleasure:1.5),(tears:1.4)",
        "clothes": "naked,rope bondage",
    },
    {
        "label": "09「絶頂の連鎖」止まらない強制絶頂",
        "scene": "forced orgasm continuation,vibrator toy attached,unable to stop climaxing,squirting repeatedly,body shaking non-stop,drugs and stimulation combined,prolonged torture by pleasure,begging to stop but unable to move",
        "pose": "full body,writhing,from front",
        "expr": "(perpetual ahegao:1.8),(squirting climax:1.5),(begging eyes:1.4)",
        "clothes": "naked,toys attached",
    },
    # 10-14: 完全な道具化・商品化
    {
        "label": "10「肉の容器」道具として認識される",
        "scene": "treated as sex object only,no eye contact made by users,mechanical use,body positioned like object,being handled without care,soul leaving expression,dissociation from own body,empty vessel,being used like furniture",
        "pose": "full body,passive position,from side",
        "expr": "(dissociated empty expression:1.6),(soul leaving:1.5),(empty vessel face:1.4)",
        "clothes": "naked,used body",
    },
    {
        "label": "11「撮影商品化」映像に残されて売られる",
        "scene": "camera recording everything,professional lighting setup for video,being filmed while used,labels and numbering applied to body,product photography style abuse,catalogued as product,no dignity remaining,commercial exploitation",
        "pose": "full body,camera angle,staged",
        "expr": "(vacant smile forced:1.5),(product face:1.4),(dead eyes smiling:1.4)",
        "clothes": "naked,numbered",
    },
    {
        "label": "12「品評会」見世物として並べられる",
        "scene": "displayed on pedestal,multiple people examining,body being appraised,touched and evaluated like object,grade stamp on body,bid being made,displayed with others similarly,complete objectification,no humanity remaining",
        "pose": "full body,standing display,from front",
        "expr": "(forced display smile:1.4),(vacant compliance:1.5),(dead inside expression:1.4)",
        "clothes": "naked,body markings",
    },
    {
        "label": "13「専用犬」四つん這いで犬として扱われる",
        "scene": "on all fours,dog collar leash,being walked,bowl on floor eating from,dog position sex from behind,completely dehumanized,crawling follows commands,whimpering like animal,human dignity completely removed",
        "pose": "full body,all fours,from side",
        "expr": "(animalistic vacant expression:1.5),(empty obedience:1.5),(feral compliance:1.4)",
        "clothes": "naked,dog collar",
    },
    {
        "label": "14「共有財産」グループの共有として管理される",
        "scene": "group ownership,being shared between multiple people,schedule posted for use times,logged as shared resource,brand mark on hip,managed systematically,no personal space,always available,permanently on call",
        "pose": "upper body,from front,collar",
        "expr": "(scheduled compliance:1.5),(programmed empty smile:1.4),(property face:1.4)",
        "clothes": "naked,brand mark,collar",
    },
    # 15-19: 極限の身体・精神崩壊
    {
        "label": "15「自我崩壊」自分が誰か完全にわからなくなる",
        "scene": "complete ego dissolution,staring at reflection not recognizing self,former identity completely gone,only drug and obedience remain,name forgotten,past life erased,new identity as property,mirror scene extreme dissociation",
        "pose": "upper body,mirror,from front",
        "expr": "(complete dissociation:1.6),(staring through mirror:1.5),(self unrecognized:1.4)",
        "clothes": "naked,unkempt",
    },
    {
        "label": "16「感覚の逆転」苦痛を快楽と感じる神経破壊",
        "scene": "pain pleasure reversal,nerve damage from drug abuse,crying tears of pleasure from pain,masochistic breakdown,begging for more pain,psychological conditioning complete,genuine arousal from suffering,broken reward system",
        "pose": "upper body,from front,in pain",
        "expr": "(pain pleasure fusion expression:1.6),(crying while aroused:1.5),(broken smile:1.4)",
        "clothes": "disheveled,marks on body",
    },
    {
        "label": "17「嘔吐と絶頂の境界」吐き続けながら絶頂する",
        "scene": "vomiting while climaxing simultaneously,body in crisis,drugs overloading system,involuntary responses beyond control,unable to stop either reaction,complete loss of bodily control,dignity completely gone,body as chaos",
        "pose": "full body,doubled over,from side",
        "expr": "(agony and ecstasy simultaneously:1.6),(body crisis expression:1.5),(out of control face:1.4)",
        "clothes": "clothes vomit soiled,disheveled",
    },
    {
        "label": "18「失禁絶頂」失禁しながら何度も絶頂する",
        "scene": "incontinence while climaxing,no bodily control remaining,completely oblivious to loss of control,puddle forming,used regardless,complete abandonment of shame,involuntary everything,beyond humiliation",
        "pose": "full body,kneeling,from front",
        "expr": "(completely shameless vacant:1.5),(unaware of own state:1.5),(beyond embarrassment:1.4)",
        "clothes": "naked,wet",
    },
    {
        "label": "19「心拍危機」心臓が止まりかけながら使われる",
        "scene": "cardiac distress,lips turning blue from drug overdose,heart monitor showing abnormal,still being used while in medical crisis,emergency ignored,prioritized as tool over health,heart rate critical,near death experience while violated",
        "pose": "full body,lying,from above",
        "expr": "(near death vacant:1.7),(blue lips:1.5),(barely conscious:1.6)",
        "clothes": "naked,medical monitor",
    },
    # 20-24: 廃人後も使われ続ける
    {
        "label": "20「反射だけ残る」条件反射のみで動く廃人",
        "scene": "complete brain damage from drugs,only conditioned reflexes remain,automatically opens mouth when approached,automatically spreads legs on command,no thought process,pure stimulus response,like doll with no one inside",
        "pose": "full body,standing empty,from front",
        "expr": "(absolute blank:1.7),(no one home expression:1.6),(pure conditioned reflex:1.5)",
        "clothes": "naked,standing vacant",
    },
    {
        "label": "21「廃人のまま連続使用」もう意識なく使われ続ける",
        "scene": "unconscious limp body still being used,no response to stimulation,positioned by others,body manipulated like doll,eyes open but seeing nothing,still warm so still useful,mechanical continued abuse,post-cognitive exploitation",
        "pose": "full body,limp,from side",
        "expr": "(empty open eyes seeing nothing:1.7),(limp unconscious:1.6),(no response:1.5)",
        "clothes": "naked,limp",
    },
    {
        "label": "22「薬液まみれ」全身が薬と体液で汚れた状態",
        "scene": "body covered in drug solution residue and bodily fluids,IV tubes still attached,syringe marks all over,dried stains,wet spots,complete filth,no attempt to clean,used as receptacle repeatedly,waste product of addiction",
        "pose": "full body,lying,from above",
        "expr": "(unconscious covered:1.5),(filth covered limp:1.4),(post-use waste:1.4)",
        "clothes": "naked,soiled,tubes attached",
    },
    {
        "label": "23「保存容器」使わない時は保管される",
        "scene": "stored in cage or container,folded compactly into small space,stored with others similarly broken,taken out when needed returned when done,no autonomy,no rest,no humanity,product storage between uses,kept alive minimally",
        "pose": "full body,cramped fetal position,from above",
        "expr": "(stored object expression:1.5),(minimal life sign:1.5),(product waiting:1.4)",
        "clothes": "naked,confined",
    },
    {
        "label": "24「永続注射」もう自分で注射を打つことだけが生きがい",
        "scene": "self-injection expert,perfect technique from practice,injecting self without hesitation,anticipating the high,track marks covering entire arms,own vein navigation,smile only for needle,everything else meaningless,living only for injection",
        "pose": "upper body,injecting self,from front",
        "expr": "(blissful injection anticipation:1.5),(only alive for this:1.5),(track mark covered arms:1.4)",
        "clothes": "disheveled,arms exposed",
    },
    # 25-29: 完全終末・消費しきった後
    {
        "label": "25「最後の意識」最後に一瞬だけ正気が戻る",
        "scene": "brief moment of lucidity before final darkness,flash of real self returning,horror at current state,tear falling from understanding,former person visible for last time,last coherent thought,then gone forever,light fading from eyes",
        "pose": "upper body,close-up,from front",
        "expr": "(last moment of real self:1.6),(horror awareness:1.5),(tear of recognition:1.4),(fading:1.3)",
        "clothes": "naked,broken",
    },
    {
        "label": "26「廃棄前使用」最後の一回として使いきられる",
        "scene": "final use before disposal,no care for aftermath,maximum exploitation,body barely surviving,used beyond limits,everything extracted,wrung out completely,nothing left to take,disposable completion,last exploitation before replacement",
        "pose": "full body,used position,from above",
        "expr": "(final use vacant:1.6),(beyond empty:1.6),(nothing left expression:1.5)",
        "clothes": "naked,destroyed",
    },
    {
        "label": "27「魂の残骸」精神が完全に砕け散った後",
        "scene": "soul completely shattered,hollow shell staring into void,all personality erased,all memories gone,all will destroyed,no emotion possible,permanent dissociation,shell breathing automatically,no recovery possible,permanent damage complete",
        "pose": "full body,sitting hollow,from front",
        "expr": "(absolute void expression:1.7),(soul completely absent:1.6),(hollow shell:1.5)",
        "clothes": "naked,sitting empty",
    },
    {
        "label": "28「肉体の限界」体が壊れ始めても止まらない",
        "scene": "body physically breaking down,multiple organ strain visible,muscle wasting extreme,eyes sunken,skin gray,still being used,medical emergency ignored,beyond endurance,physical limits destroyed,kept alive by drugs alone",
        "pose": "full body,deteriorated,from front",
        "expr": "(near death physical:1.6),(hollow organ failure:1.5),(barely alive expression:1.5)",
        "clothes": "naked,deteriorated body",
    },
    {
        "label": "29「空の器に何を注いでも」もう何も感じない完全な廃人",
        "scene": "absolute zero state,no drug effect possible,no stimulation response,no pleasure no pain,just biological functions remaining,eyes completely empty,used regardless,container with no contents,beyond all,final state",
        "pose": "full body,empty lying,from above",
        "expr": "(absolute zero expression:1.8),(total emptiness:1.7),(beyond ahegao beyond everything:1.6)",
        "clothes": "naked,final state",
    },
]

# =========================================================
# outfit JS生成関数
# =========================================================

def make_outfit(scene_data, base_prompt, char_name):
    label = scene_data["label"]
    scene = scene_data["scene"]
    pose = scene_data["pose"]
    expr = scene_data["expr"]
    clothes = scene_data.get("clothes", "")
    
    value = (
        f"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),"
        f"{base_prompt},"
        f"(drugged high:1.8),(heavily drugged:1.7),(drug overdose state:1.6),"
        f"{expr},"
        f"{scene},"
        f"{pose},"
        f"dim room,dim lighting,{COMMON_QUALITY}"
    )
    # JS文字列のエスケープ（シングルクォート）
    label_esc = label.replace("'", "\\'")
    value_esc = value.replace("'", "\\'")
    return f"{{'label':'{label_esc}','value':'{value_esc}'}}"

# =========================================================
# ティファ S3 outfits生成
# =========================================================
tifa_outfits = [make_outfit(s, TIFA_BASE, "Tifa") for s in S3_SCENES]
tifa_outfits_js = "[" + ",".join(tifa_outfits) + "]"

# =========================================================
# エアリス S3 outfits生成（シーンは同じ、ベースプロンプトが違う）
# =========================================================
aerith_outfits = [make_outfit(s, AERITH_BASE, "Aerith") for s in S3_SCENES]
aerith_outfits_js = "[" + ",".join(aerith_outfits) + "]"

# =========================================================
# dashboard.html の S3_tifa と S3_aerith の outfits を置換
# =========================================================

# 現在のS3_tifaのoutfitsを取得して位置を特定
def replace_outfits(html, char_id, new_outfits_js):
    idx = html.find(f"id:'{char_id}'")
    if idx < 0:
        idx = html.find(f"id: '{char_id}'")
    if idx < 0:
        return html, False
    
    # outfits:[ を探す
    oi = html.find("outfits:", idx)
    if oi < 0 or oi - idx > 5000:
        return html, False
    
    start = html.find('[', oi)
    if start < 0:
        return html, False
    
    # ネストを追跡して閉じ括弧を探す
    depth = 0
    end = start
    in_string = False
    string_char = None
    i = start
    while i < len(html):
        c = html[i]
        if in_string:
            if c == '\\':
                i += 2
                continue
            if c == string_char:
                in_string = False
        else:
            if c in ('"', "'"):
                in_string = True
                string_char = c
            elif c == '[':
                depth += 1
            elif c == ']':
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        i += 1
    
    old_outfits = html[start:end]
    new_html = html[:start] + new_outfits_js + html[end:]
    print(f"  {char_id}: outfits replaced ({len(old_outfits)} -> {len(new_outfits_js)} bytes)")
    return new_html, True

# バックアップ
import shutil, datetime
backup_name = r'C:\AI\ComfyUI\dashboard_backup_s3ff_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html'
shutil.copy2(path, backup_name)
print(f"Backup: {backup_name}")

# 置換実行
content, ok1 = replace_outfits(content, 'char_kakuseizai_s3_ff_tifa', tifa_outfits_js)
if ok1:
    print("Tifa S3 outfits: OK")
else:
    print("Tifa S3 outfits: FAILED")

content, ok2 = replace_outfits(content, 'char_kakuseizai_s3_ff_aerith', aerith_outfits_js)
if ok2:
    print("Aerith S3 outfits: OK")
else:
    print("Aerith S3 outfits: FAILED")

# バージョン更新
import re as _re
ver_m = _re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1)
    new_ver = str(int(old_ver) + 1)
    content = content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f"Version: {old_ver} -> {new_ver}")

# 保存
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"Saved: {path}")
print(f"Scenes per char: {len(S3_SCENES)}")
