"""
実データ130タグを完全解析して dedupe_groups / conflicts / rewrites を最強版で定義する。
全WF（real/anime/panel）共通。
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# =============================================================================
# dedupe_groups
# require=[] / any=完全一致リスト / 同グループ内は最高重みの1つだけ残す
# =============================================================================
DEDUPE_GROUPS = [

    # ---- 人数タグ（solo/1girl/only one person 等） ----
    {"name":"people_count","require":[],"any":[
        "1girl","2girls","3girls","4girls","5girls","multiple girls","many girls",
        "solo","duo","trio","group","couple","harem",
        "only one person","one person","single person","1 person",
        "solo female only","only female subject visible in frame",
        "one girl","one woman","single girl","just one girl",
    ]},

    # ---- 単一頭部・身体の整合性タグ ----
    {"name":"single_head","require":[],"any":[
        "single head","one head","only one head",
        "one face","one face only","no duplicate face","no extra face","no extra head",
        "no second head","no multiple faces","symmetrical single head",
        "coherent single body","coherent body","consistent body",
        "no clone","no doppelganger",
    ]},

    # ---- 解剖学的正確さ ----
    {"name":"anatomically_correct","require":[],"any":[
        "anatomically correct","anatomically correct female","female anatomy",
        "correct anatomy","realistic anatomy","proper anatomy","anatomical",
        "anatomically accurate",
    ]},

    # ---- 写真リアリズム ----
    {"name":"photo_realism","require":[],"any":[
        "photorealistic","photo realistic","hyperrealistic","hyper realistic",
        "photoreal","photo-realistic","ultra realistic","highly realistic",
    ]},

    # ---- RAW写真感 ----
    {"name":"raw_photo","require":[],"any":[
        "raw photo","raw image","raw photograph","unedited photo",
        "straight out of camera","unprocessed photo",
    ]},

    # ---- 写真・画像タイプ ----
    {"name":"photo_type","require":[],"any":[
        "photograph","photography","photo","snapshot","candid photo",
        "real photo","actual photo","taken photo",
    ]},

    # ---- リアル人物タグ ----
    {"name":"real_person","require":[],"any":[
        "real person","actual person","real human","real woman","real girl",
        "real life person","looks like real person",
    ]},

    # ---- カメラ機材 ----
    {"name":"camera_type","require":[],"any":[
        "dslr","slr camera","mirrorless camera","digital camera",
        "35mm camera","film camera","shot on dslr","shot on film",
        "shot on camera","canon eos","nikon","sony a7",
    ]},

    # ---- フィルムグレイン・ノイズ（重複になりやすい） ----
    {"name":"film_grain","require":[],"any":[
        "film grain","grainy","grain","noise","film noise","analog grain",
        "film texture","cinematic grain",
    ]},

    # ---- 品質ブースト（ultra/highly/extremely detailed 等） ----
    {"name":"quality_boost","require":[],"any":[
        "ultra-detailed","ultra detailed","highly detailed","intricate details",
        "extremely detailed","super detailed","insanely detailed","very detailed",
        "incredible detail","maximum detail","exquisite detail",
        "8k resolution","8k","16k","4k","hd","full hd","high definition",
        "high resolution","hi-res","highres","high res",
    ]},

    # ---- シャープネス ----
    {"name":"sharpness","require":[],"any":[
        "sharp focus","tack sharp","tack-sharp","crystal clear","crisp details","crisp",
        "pin sharp","razor sharp","fine detail","perfect focus","in focus",
        "razor-sharp","needle sharp",
    ]},

    # ---- 肌テクスチャ ----
    {"name":"skin_detail","require":[],"any":[
        "realistic skin texture","detailed skin texture","skin texture",
        "skin pores","visible skin pores","pore texture","open pores",
        "subsurface scattering","subsurface","skin translucency","skin detail",
        "natural skin texture","authentic skin",
    ]},

    # ---- 顔の詳細 ----
    {"name":"face_detail","require":[],"any":[
        "detailed facial features","detailed face","face detail",
        "sharp detailed eyes","detailed eyes","eye detail",
        "beautiful detailed face","highly detailed face",
    ]},

    # ---- 民族・顔の国籍 ----
    {"name":"ethnicity_face","require":[],"any":[
        "pure japanese ethnicity","japanese ethnicity","japanese face",
        "authentic japanese facial features","japanese girl face","japanese features",
        "pure japanese","east asian face","east asian ethnicity",
        "asian face","asian ethnicity","asian features",
        "korean face","chinese face","monolid","almond eyes","japanese eyes",
        "japanese skin tone","asian skin tone","east asian appearance",
        "no western features","no caucasian features",
    ]},

    # ---- かわいい系 ----
    {"name":"cute_appeal","require":[],"any":[
        "cute","adorable","kawaii","charming face","lovely","sweet face",
        "dainty","precious face","endearing","cutie","charming",
    ]},

    # ---- 胸サイズ ----
    {"name":"breast_size","require":[],"any":[
        "flat chest","no breasts","small breasts","tiny breasts","petite breasts",
        "medium breasts","average breasts","moderate breasts","normal breasts","natural breast shape",
        "large breasts","big breasts","full breasts","ample breasts",
        "huge breasts","very large breasts","enormous breasts","massive breasts",
        "gigantic breasts","colossal breasts","hyper breasts","oversized breasts",
        "a-cup","b-cup","c-cup","d-cup","e-cup","f-cup","g-cup","h-cup","i-cup","j-cup","k-cup",
        "breast implants","breast augmentation","augmented breasts","implants",
    ]},

    # ---- 体型 ----
    {"name":"body_build","require":[],"any":[
        "slender body","slim body","thin body","lean body","petite body",
        "athletic body","toned body","small body","tiny body","compact body",
        "muscular body","stocky body","curvy body","chubby body","plump body",
        "slender build","slim build","athletic build","petite build","lean build",
        "small stature","short stature","petite stature",
        "small frame","slender frame","slim frame","slight frame",
        "lithe figure","willowy figure","svelte figure","petite figure",
    ]},

    # ---- 構図フレーミング ----
    {"name":"frame_type","require":[],"any":[
        "full body","full body shot","whole body","entire body","full shot","full-body",
        "upper body","upper body shot","bust shot","half body","half-body shot",
        "cowboy shot","medium shot","three-quarter shot","3/4 shot",
        "waist up","waist-up","from waist up",
        "lower body","lower body shot","lower half",
        "wide shot","long shot","extreme long shot","full wide shot",
        "close-up","close up","extreme close-up","macro shot","tight shot",
        "portrait","portrait shot","head shot","headshot","face shot",
        "head and shoulders","chest shot","torso shot",
        "upper body naturally clothed","upper body fully clothed",
    ]},

    # ---- 撮影角度 ----
    {"name":"camera_angle","require":[],"any":[
        "eye level","eye-level","at eye level","straight on","frontal view","front view",
        "high angle","high angle shot","from above","bird's eye","bird eye view",
        "overhead view","top down","overhead shot","top-down view",
        "low angle","low angle shot","from below","worm's eye","worm eye view",
        "ground level shot","upward angle",
        "from front","from side","side view","profile view","profile shot",
        "from behind","back view","rear view","posterior view","rear shot",
        "dutch angle","tilted angle","canted angle","diagonal angle",
        "over the shoulder","over shoulder shot",
    ]},

    # ---- 奥行き・ボケ ----
    {"name":"depth_of_field","require":[],"any":[
        "shallow depth of field","depth of field","bokeh","background bokeh",
        "blurred background","out of focus background","soft background",
        "background blur","defocused background","selective focus",
    ]},

    # ---- 照明 ----
    {"name":"lighting_type","require":[],"any":[
        "natural light","natural lighting","window light","sunlight","daylight","sun light",
        "soft light","soft lighting","diffused light","diffuse lighting",
        "even lighting","even natural lighting","flat lighting","balanced lighting",
        "studio light","studio lighting","professional lighting","studio setup",
        "rim light","rim lighting","edge light","hair light",
        "backlight","backlighting","contre-jour",
        "side light","side lighting","rembrandt lighting","three point lighting",
        "candlelight","candlelit","firelight","fire light",
        "moonlight","moonlit","night light",
        "dim lighting","low light","low key lighting","moody lighting",
        "dramatic lighting","chiaroscuro","high contrast lighting",
        "warm lighting","warm light","cool lighting","cool light",
        "spotlight","spot light","key light",
    ]},

    # ---- 表情の一貫性 ----
    {"name":"expression_consistency","require":[],"any":[
        "consistent single expression","consistent expression","expression consistent",
        "one expression","single expression","expression coherent",
        "uniform expression","stable expression",
    ]},

    # ---- アヘ顔・目の状態 ----
    {"name":"eye_state","require":[],"any":[
        "rolled back eyes","eyes rolled back","rolling eyes","eyes rolling",
        "pupils rolled up","white eyes","showing whites","blank eyes",
        "dilated pupils","constricted pupils","slit pupils",
        "empty eyes","hollow eyes","unfocused eyes","glazed eyes","blank stare",
        "crossed eyes","spinning eyes",
    ]},

    # ---- 唾液・涎 ----
    {"name":"drool_type","require":[],"any":[
        "drooling","drooling saliva","drool","saliva dripping","saliva trail",
        "drool string","drool dripping","saliva string","mouth drool",
        "slobbering","excessive drooling","uncontrollable drool",
    ]},

    # ---- 着衣保証（トップス） ----
    {"name":"clothed_top","require":[],"any":[
        "upper body naturally clothed","upper body fully clothed",
        "top stays on","chest covered by clothing","chest covered",
        "breasts covered","top garment covering torso","shirt stays on",
        "clothed upper body","torso clothed","outfit on top",
        "top on","wearing top","wearing shirt","shirt on","blouse on",
    ]},

    # ---- 着衣保証（ボトムス） ----
    {"name":"clothed_bottom","require":[],"any":[
        "lower body fully clothed","skirt or pants worn","lower body clothed",
        "hips and crotch covered by clothing","fully covered crotch",
        "fabric over crotch","legs covered","bottom stays on",
        "pants stays on","skirt stays on","lower body still clothed",
        "wearing skirt","wearing pants","skirt on","pants on",
    ]},

    # ---- 着衣全般 ----
    {"name":"clothed_full","require":[],"any":[
        "fully clothed","clothing stays on","clothing intact","outfit intact",
        "outfit consistent with described clothing","clothes on","outfit stays on",
        "dressed properly","wearing clothes","outfit on","fully dressed",
    ]},

    # ---- パンツ・下着タイプ ----
    {"name":"panty_type","require":[],"any":[
        "realistic everyday panties","ordinary cotton underwear","amateur realistic underwear",
        "cotton panties","white panties","plain panties","simple underwear",
        "everyday underwear","women's underwear","female panties","women's panties",
        "women underwear","plain white panties","school uniform panties",
    ]},

    # ---- パイパン・陰毛なし ----
    {"name":"pubic_hair_state","require":[],"any":[
        "smooth hairless pubic area","no pubic hair","hairless pubic area",
        "shaved pussy","hairless pussy","bald pussy","smooth pubic",
        "clean shaved","waxed","bare pubic","pubic hair removed",
    ]},

    # ---- 乱れた髪（重複） ----
    {"name":"disheveled_hair","require":[],"any":[
        "slightly disheveled hair","hair slightly messed","disheveled hair",
        "messed hair","messy hair","hair in disarray","unkempt hair",
        "tousled hair","ruffled hair","windswept hair",
    ]},

    # ---- 発汗・体の状態 ----
    {"name":"sweating","require":[],"any":[
        "sweating","sweaty","covered in sweat","dripping sweat","perspiring",
        "glistening with sweat","sweat beads","sweat on skin","drenched in sweat",
    ]},

    # ---- 呼吸・喘ぎ ----
    {"name":"breathing","require":[],"any":[
        "heavy breathing","panting","gasping","labored breathing","rapid breathing",
        "out of breath","breathless","hyperventilating","shallow breathing",
    ]},

    # ---- 薬物・ハイ状態 ----
    {"name":"drugged_state","require":[],"any":[
        "drugged high","drugged","high on drugs","drug effect","under the influence",
        "sedated","narcotic effect","chemically induced","drug induced",
    ]},

    # ---- 服の一貫性タグ ----
    {"name":"outfit_consistency","require":[],"any":[
        "outfit consistent with described clothing","clothing consistent",
        "consistent outfit","outfit as described","wearing described outfit",
        "outfit matches description",
    ]},

    # ---- マスターピース/ベスト品質 ----
    {"name":"masterpiece","require":[],"any":[
        "masterpiece","best quality","top quality","highest quality",
        "exceptional quality","premium quality","superior quality",
        "award winning","gallery quality",
    ]},

    # ---- 見えている主体・クリア ----
    {"name":"clear_subject","require":[],"any":[
        "clear visible subject","subject clearly visible","clear shot",
        "unobstructed view","clear view of subject","subject in focus",
        "well lit subject","clearly visible",
    ]},
]

# =============================================================================
# conflicts — 矛盾タグ解消（prefer: "a"=a側残す, "b"=b側残す, "weighted"=重み大を残す）
# =============================================================================
CONFLICTS = [
    # ---- 全裸 vs 着衣 ----
    {"name":"nude_vs_clothed","prefer":"b",
     "a":["nude","naked","fully nude","completely naked","undressed","bare body",
          "no clothes","without clothes","unclothed","stripped naked","exposed body","disrobed"],
     "b":["fully clothed","clothed","dressed","wearing clothes","outfit on",
          "clothing intact","clothes on","upper body fully clothed","lower body fully clothed",
          "outfit stays on","fully dressed"]},

    # ---- トップレス vs トップス着用 ----
    {"name":"topless_vs_top_on","prefer":"b",
     "a":["topless","bare chest","no shirt","no top","bare breasts","exposed chest",
          "chest exposed","shirt off","shirt removed","top removed","naked chest"],
     "b":["top stays on","chest covered","breasts covered","upper body naturally clothed",
          "upper body fully clothed","wearing shirt","shirt on","blouse on","top on"]},

    # ---- ノーパン vs パンツあり ----
    {"name":"pantless_vs_panty_on","prefer":"b",
     "a":["no panties","pantyless","bottomless","no underwear","panties removed","underwear off"],
     "b":["wearing panties","panties under skirt","visible panties",
          "lower body fully clothed","fabric over crotch","fully covered crotch",
          "skirt on","pants on"]},

    # ---- full body vs 顔クローズアップ ----
    {"name":"fullbody_vs_face_closeup","prefer":"a",
     "a":["full body","full body shot","whole body","entire body","full shot"],
     "b":["close-up face","extreme close-up face","face only","portrait crop",
          "head only","face fills frame","face fill frame","cropped at neck",
          "face close up","close up of face","extreme face closeup"]},

    # ---- upper body vs extreme close-up ----
    {"name":"upperbody_vs_extreme_closeup","prefer":"a",
     "a":["upper body","upper body shot","bust shot","upper body naturally clothed"],
     "b":["extreme close-up","extreme closeup","macro shot","face macro",
          "close-up of face","face close-up","close up face","macro face shot"]},

    # ---- eye level vs 矛盾する角度 ----
    {"name":"angle_eyevel_vs_high","prefer":"a",
     "a":["eye level","eye-level"],
     "b":["high angle shot","bird's eye view","overhead shot","top down view",
          "from directly above","overhead angle"]},

    {"name":"angle_eyevel_vs_low","prefer":"a",
     "a":["eye level","eye-level"],
     "b":["worm's eye view","from directly below","extreme low angle","ground level looking up"]},

    # ---- standing vs lying ----
    {"name":"stand_vs_lie","prefer":"weighted",
     "a":["standing","standing pose","standing upright","standing position","standing up"],
     "b":["lying down","lying on back","lying on stomach","lying on floor",
          "on back","on stomach","supine","prone position","recumbent","laid out"]},

    # ---- sitting vs lying ----
    {"name":"sit_vs_lie","prefer":"weighted",
     "a":["sitting","seated","sitting position","sitting pose"],
     "b":["lying down","lying on back","lying flat","recumbent"]},

    # ---- 笑顔 vs 痛み表情 ----
    {"name":"smile_vs_pain","prefer":"b",
     "a":["smiling","happy smile","big smile","cheerful smile","laughing",
          "grinning","beaming","joyful expression","happy face","bright smile"],
     "b":["pained expression","grimacing","suffering face","agony","wincing",
          "anguish","distressed face","tightly shut eyes","clenched teeth",
          "furrowed brow in pain","pain face"]},

    # ---- 笑顔/平静 vs ahegao ----
    {"name":"calm_vs_ahegao","prefer":"b",
     "a":["smiling","happy smile","cheerful","joyful expression","calm face",
          "neutral expression","relaxed face","serene face","composed face",
          "stoic","expressionless","resting face"],
     "b":["ahegao","mind break","mind blown","eyes rolling back","rolled back eyes",
          "tongue hanging out","drooling uncontrollably","pleasure overload",
          "completely broken expression"]},

    # ---- 意識あり vs 意識なし ----
    {"name":"conscious_vs_unconscious","prefer":"b",
     "a":["awake","conscious","aware","alert","responsive","eyes open and aware"],
     "b":["unconscious","passed out","fainted","limp body","completely unconscious",
          "knocked out","out cold","unresponsive","eyes closed unconscious"]},

    # ---- 平静/落ち着き vs 強い表情全般 ----
    {"name":"calm_vs_intense_expression","prefer":"b",
     "a":["calm face","neutral expression","stoic","expressionless","blank face",
          "resting face","composed","placid face","serene"],
     "b":["ahegao","orgasm face","screaming","crying loudly","terrified",
          "pained expression","euphoric","overwhelmed","ecstatic","hysterical",
          "in agony","pleasure face","climax face"]},

    # ---- no sexual activity vs 性行為 ----
    {"name":"nosex_vs_sex","prefer":"b",
     "a":["no sexual activity","non-sexual","sfw","safe for work","no explicit content"],
     "b":["penetration","insertion visible","vaginal sex","anal sex","oral sex",
          "blowjob","handjob","sex act","intercourse","fucking","sexual intercourse"]},

    # ---- 服が消える vs 着衣維持 ----
    {"name":"clothes_vanish_vs_clothed","prefer":"b",
     "a":["magically naked","suddenly nude","clothes disappeared","outfit vanishes",
          "clothing disappeared","clothes removed","accidental undressing",
          "wardrobe malfunction"],
     "b":["fully clothed","clothing intact","outfit intact","clothing stays on",
          "outfit stays on","clothes on"]},

    # ---- 複数人 vs solo ----
    {"name":"multi_vs_solo","prefer":"b",
     "a":["2girls","3girls","4girls","multiple girls","two girls","three girls",
          "group of girls","duo","trio","crowd","many people","multiple people"],
     "b":["1girl","solo","only one person","single girl","one girl",
          "solo female only","only female subject visible in frame"]},
]

# =============================================================================
# rewrites — a+b同居時に両方削除して replace に置換
# =============================================================================
REWRITES = [
    # 痛み + 瞳孔散大 → 痛み表情に統合
    {"name":"pain_dilated_pupils","replace":[
        "(pained expression:1.5)","(tightly shut eyes:1.4)",
        "(clenched teeth:1.4)","(dilated pupils:1.5)","(pale face:1.3)"],
     "a":["pained expression","grimacing","suffering face","wincing in pain"],
     "b":["dilated pupils","wide pupils","expanded pupils"]},

    # ahegao + 瞳孔散大 → 完全なアヘ顔に統合
    {"name":"ahegao_dilated","replace":[
        "(ahegao:1.8)","(rolled back eyes:1.7)","(tongue sticking out:1.6)",
        "(drooling saliva:1.6)","(dilated pupils:1.6)","(flushed face:1.5)"],
     "a":["ahegao","eyes rolling back","rolled back eyes"],
     "b":["dilated pupils","wide pupils"]},
]

# =============================================================================
# 書き込み
# =============================================================================
with open(r'C:\AI\ComfyUI\quality_rules\real.json', encoding='utf-8') as f:
    real = json.load(f)

real['dedupe_groups'] = DEDUPE_GROUPS
real['conflicts']     = CONFLICTS
real['rewrites']      = REWRITES
real['conflict_neg']  = [
    "(contradictory outfit state:1.5)",
    "(inconsistent clothing:1.5)",
]

with open(r'C:\AI\ComfyUI\quality_rules\real.json', 'w', encoding='utf-8') as f:
    json.dump(real, f, ensure_ascii=False, indent=2)

# _common.json（全WF共通サブセット）
with open(r'C:\AI\ComfyUI\quality_rules\_common.json', encoding='utf-8') as f:
    common = json.load(f)

COMMON_DEDUPE_NAMES = {
    'people_count','single_head','anatomically_correct','quality_boost','sharpness',
    'cute_appeal','expression_consistency','drool_type','eye_state',
    'disheveled_hair','sweating','breathing','masterpiece','clear_subject',
    'multi_vs_solo',
}
COMMON_CONFLICT_NAMES = {
    'nude_vs_clothed','topless_vs_top_on','pantless_vs_panty_on',
    'smile_vs_pain','calm_vs_ahegao','conscious_vs_unconscious',
    'calm_vs_intense_expression','nosex_vs_sex','clothes_vanish_vs_clothed',
    'multi_vs_solo',
}

if 'rules' not in common:
    common['rules'] = {}
common['rules']['dedupe_groups'] = [g for g in DEDUPE_GROUPS if g['name'] in COMMON_DEDUPE_NAMES]
common['rules']['conflicts']     = [c for c in CONFLICTS if c['name'] in COMMON_CONFLICT_NAMES]
common['rules']['rewrites']      = REWRITES

with open(r'C:\AI\ComfyUI\quality_rules\_common.json', 'w', encoding='utf-8') as f:
    json.dump(common, f, ensure_ascii=False, indent=2)

print(f"real.json:")
print(f"  dedupe_groups: {len(DEDUPE_GROUPS)}")
print(f"  conflicts:     {len(CONFLICTS)}")
print(f"  rewrites:      {len(REWRITES)}")
print(f"_common.json:")
print(f"  dedupe_groups: {len([g for g in DEDUPE_GROUPS if g['name'] in COMMON_DEDUPE_NAMES])}")
print(f"  conflicts:     {len([c for c in CONFLICTS if c['name'] in COMMON_CONFLICT_NAMES])}")
print("DONE")
