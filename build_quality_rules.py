"""
全WF向け quality_rules/real.json と _common.json に
dedupe_groups / conflicts / rewrites を完全定義する。

設計方針:
- dedupe_groups: 同カテゴリ内で複数タグが存在する場合、最高重みの1つだけ残す
- conflicts: 意味的に矛盾する組み合わせを解消
- rewrites: a群+b群の同居を1つの正確なタグに統合
"""
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

# ===== dedupe_groups =====
# require: これらのキーワードが1つ以上含まれる場合のみグループとして判定
# any: このリスト内キーワードにマッチするタグが対象
# 同グループ内に複数タグがある場合: prio > 高重み > 後出し の順で1つだけ残す

DEDUPE_GROUPS = [
    # ---- 人数 ----
    {
        "name": "people_count",
        "any": ["1girl","2girls","3girls","4girls","5girls","multiple girls",
                "1boy","2boys","solo","duo","trio","group","couple","pair",
                "only one person","one person","single person","one girl","one woman"],
    },
    # ---- 一人強調 ----
    {
        "name": "solo_emphasis",
        "any": ["solo focus","solo female only","only female subject","single subject",
                "subject only","one subject in frame","only one girl"],
    },
    # ---- 体型・体格 ----
    {
        "name": "body_build",
        "any": ["slender body","slim body","thin body","lean body","petite body",
                "athletic body","toned body","small body","tiny body","compact body",
                "muscular body","stocky body","curvy body","chubby body","plump body",
                "slender","slim","thin","lean","petite","athletic","toned",
                "skinny","lithe","wiry","compact","willowy","svelte"],
    },
    # ---- 胸サイズ ----
    {
        "name": "breast_size",
        "any": ["flat chest","no breasts","small breasts","tiny breasts","petite breasts",
                "medium breasts","average breasts","moderate breasts","normal breasts",
                "large breasts","big breasts","full breasts","ample breasts",
                "huge breasts","very large breasts","enormous breasts","massive breasts",
                "gigantic breasts","colossal breasts","hyper breasts",
                "a-cup","b-cup","c-cup","d-cup","e-cup","f-cup","g-cup","h-cup",
                "i-cup","j-cup","k-cup","natural breast shape","natural breasts"],
    },
    # ---- 肌の詳細（テクスチャ系） ----
    {
        "name": "skin_detail",
        "any": ["realistic skin texture","detailed skin texture","skin texture",
                "skin pores","visible skin pores","pore texture",
                "subsurface scattering","subsurface","skin translucency"],
    },
    # ---- 高解像度・品質ブースト（テクスチャ系以外） ----
    {
        "name": "quality_boost",
        "any": ["ultra-detailed","ultra detailed","highly detailed","intricate details",
                "extremely detailed","super detailed","insanely detailed",
                "8k resolution","8k","16k","4k","hd","full hd","high definition",
                "high resolution","hi-res","highres"],
    },
    # ---- シャープネス ----
    {
        "name": "sharpness",
        "any": ["sharp focus","tack sharp","crystal clear","crisp details","crisp",
                "in focus","perfect focus","pin sharp","razor sharp","fine detail"],
    },
    # ---- 写真リアリズム ----
    {
        "name": "photo_realism",
        "any": ["photorealistic","photo realistic","hyperrealistic","hyper realistic",
                "realistic","lifelike","true to life","photoreal"],
    },
    # ---- カメラ機材 ----
    {
        "name": "camera_type",
        "any": ["dslr","slr","mirrorless","digital camera","35mm","film camera",
                "shot on dslr","shot on film","canon","nikon","sony camera"],
    },
    # ---- 生写真感 ----
    {
        "name": "raw_photo",
        "any": ["raw photo","raw image","raw photograph","unedited photo",
                "straight out of camera","jpeg artifact"],
    },
    # ---- 顔の民族・国籍 ----
    {
        "name": "ethnicity_face",
        "any": ["pure japanese ethnicity","japanese face","authentic japanese facial features",
                "japanese girl face","asian face","east asian face","japanese skin tone",
                "monolid","almond eyes","japanese eyes","korean face","chinese face",
                "asian ethnicity","japanese ethnicity"],
    },
    # ---- 単一頭部保証 ----
    {
        "name": "single_head",
        "any": ["single head","one head","only one head","one face","one face only",
                "no duplicate face","no extra face","no second head","no extra head",
                "symmetrical single head","coherent single body","coherent body",
                "no multiple faces"],
    },
    # ---- 解剖学的正確さ ----
    {
        "name": "anatomically_correct",
        "any": ["anatomically correct","anatomically correct female","female anatomy",
                "correct anatomy","realistic anatomy","proper anatomy"],
    },
    # ---- 構図フレーミング ----
    {
        "name": "frame_type",
        "any": ["full body","full body shot","whole body","entire body","full shot",
                "upper body","upper body shot","bust shot","half body",
                "cowboy shot","medium shot","waist up","waist-up",
                "lower body","lower half shot",
                "wide shot","long shot","extreme long shot",
                "close-up","close up","extreme close-up","macro shot",
                "portrait","head shot","headshot","face shot","head and shoulders",
                "torso shot","chest shot"],
    },
    # ---- 撮影角度 ----
    {
        "name": "camera_angle",
        "any": ["eye level","eye-level","straight on","frontal view",
                "high angle","from above","bird's eye","overhead view","top down",
                "low angle","from below","worm's eye","ground level",
                "from front","from side","side view","profile view",
                "from behind","back view","rear view","posterior view",
                "dutch angle","tilted angle","diagonal angle"],
    },
    # ---- 奥行き・深度 ----
    {
        "name": "depth_of_field",
        "any": ["shallow depth of field","depth of field","bokeh","blurred background",
                "out of focus background","soft background","background blur"],
    },
    # ---- 照明タイプ ----
    {
        "name": "lighting_type",
        "any": ["natural light","natural lighting","window light","sunlight","daylight",
                "soft light","soft lighting","diffused light","even lighting",
                "studio light","studio lighting","professional lighting",
                "rim light","rim lighting","backlight","backlighting",
                "side light","side lighting","three point lighting",
                "candlelight","candlelit","firelight","moonlight","moonlit",
                "dim lighting","low light","low key lighting","moody lighting",
                "dramatic lighting","spotlight","harsh lighting",
                "warm light","cool light","even natural lighting"],
    },
    # ---- 女性顔の詳細 ----
    {
        "name": "face_detail",
        "any": ["detailed facial features","detailed face","detailed eyes",
                "sharp detailed eyes","beautiful face","pretty face",
                "perfect face","flawless face"],
    },
    # ---- かわいい系 ----
    {
        "name": "cute_appeal",
        "any": ["cute","adorable","kawaii","charming","lovely","sweet",
                "dainty","precious","endearing","delightful"],
    },
    # ---- 着衣保証（同義タグ群） ----
    {
        "name": "clothed_assurance_top",
        "any": ["upper body naturally clothed","upper body fully clothed",
                "top stays on","chest covered by clothing","chest covered",
                "breasts covered","top garment covering torso","shirt stays on",
                "clothed upper body","torso clothed","outfit on top"],
    },
    {
        "name": "clothed_assurance_bottom",
        "any": ["lower body fully clothed","skirt or pants worn","lower body clothed",
                "hips and crotch covered by clothing","fully covered crotch",
                "fabric over crotch","legs covered","bottom stays on",
                "pants stays on","skirt stays on","lower body still clothed"],
    },
    {
        "name": "clothed_assurance_full",
        "any": ["fully clothed","clothing stays on","clothing intact","outfit intact",
                "outfit consistent with described clothing","clothes on",
                "outfit stays on","dressed","dressed properly"],
    },
    # ---- パンツ系（同義） ----
    {
        "name": "panty_type",
        "any": ["realistic everyday panties","ordinary cotton underwear",
                "amateur realistic underwear","cotton panties","white panties",
                "plain panties","simple underwear","everyday underwear"],
    },
    # ---- 表情一貫性 ----
    {
        "name": "expression_consistency",
        "any": ["consistent single expression","consistent expression",
                "one expression","single expression","expression consistent"],
    },
    # ---- 目の状態（矛盾しやすい） ----
    {
        "name": "eye_direction",
        "any": ["eyes cast downward","looking down","downcast eyes","downward gaze",
                "eyes up","looking up","upward gaze","eyes forward",
                "eyes to side","sideways glance","avoiding eye contact",
                "looking away","eyes closed","closed eyes"],
    },
    # ---- 唾液・口 ----
    {
        "name": "drool_type",
        "any": ["drooling","drooling saliva","drool","saliva dripping","saliva trail",
                "drool string","slobbering","excessive drooling"],
    },
    # ---- 目の白目・瞳 ----
    {
        "name": "eye_state",
        "any": ["rolled back eyes","pupils rolled up","rolling eyes","eyes rolling",
                "eyes rolled back","white eyes","showing whites",
                "dilated pupils","constricted pupils","blank eyes","hollow eyes",
                "empty eyes","unfocused eyes","glazed eyes"],
    },
]

# ===== conflicts =====
# a群とb群が同居した場合、重み大/charlock優先側を残してもう一方を削除

CONFLICTS = [
    # ---- 全裸 vs 着衣 ----
    {
        "name": "nude_vs_clothed",
        "a": ["nude","naked","fully nude","completely naked","undressed","bare body",
              "no clothes","without clothes","unclothed","stripped","exposed body"],
        "b": ["fully clothed","clothed","dressed","wearing clothes","outfit on",
              "clothing intact","clothes on","upper body fully clothed","lower body fully clothed"],
        "prefer": "b",
    },
    # ---- トップレス vs トップス着用 ----
    {
        "name": "topless_vs_top_on",
        "a": ["topless","bare chest","no shirt","no top","bare breasts","exposed chest",
              "chest exposed","shirt off","shirt removed"],
        "b": ["top stays on","chest covered","breasts covered","upper body naturally clothed",
              "upper body fully clothed","wearing shirt","shirt on","blouse on"],
        "prefer": "b",
    },
    # ---- パンツなし vs パンツあり ----
    {
        "name": "pantless_vs_panty",
        "a": ["no panties","pantyless","bottomless","no underwear"],
        "b": ["wearing panties","panties under skirt","visible panties",
              "lower body fully clothed","fabric over crotch","fully covered crotch"],
        "prefer": "b",
    },
    # ---- 挿入あり vs 着衣下半身 ----
    # ※ 着衣セックスシーンでは意図的な共存なのでスキップ対象（既存ロジックで除外済み）
    # ---- full body vs close-up（顔）----
    {
        "name": "fullbody_vs_face_closeup",
        "a": ["full body","full body shot","whole body","entire body"],
        "b": ["close-up face","extreme close-up face","face only","portrait crop",
              "head only","face fills frame","face fill frame","cropped at neck"],
        "prefer": "a",
    },
    # ---- upper body vs extreme close-up ----
    {
        "name": "upperbody_vs_extreme_closeup",
        "a": ["upper body","upper body shot","bust shot"],
        "b": ["extreme close-up","macro shot","face macro","close-up of face",
              "face close-up","close up face"],
        "prefer": "a",
    },
    # ---- eye level vs from above/below（矛盾角度） ----
    {
        "name": "angle_contradiction",
        "a": ["eye level","eye-level","straight on angle"],
        "b": ["high angle shot","from above","bird's eye view","overhead shot",
              "top down view","worm's eye","from below","low angle shot"],
        "prefer": "a",
    },
    # ---- standing vs lying ----
    {
        "name": "pose_contradiction_stand_lie",
        "a": ["standing","standing pose","standing upright","standing position"],
        "b": ["lying down","lying on back","lying on stomach","lying on floor",
              "on back","on stomach","supine","prone position"],
        "prefer": "weighted",
    },
    # ---- 笑顔 vs 苦痛表情 ----
    {
        "name": "expression_smile_vs_pain",
        "a": ["smiling","happy smile","big smile","cheerful smile","laughing",
              "grinning","beaming","joyful expression","happy face"],
        "b": ["pained expression","grimacing","suffering face","agony","crying in pain",
              "anguish","distressed face","tightly shut eyes","clenched teeth"],
        "prefer": "b",
    },
    # ---- 笑顔 vs ahegao ----
    {
        "name": "expression_smile_vs_ahegao",
        "a": ["smiling","happy smile","cheerful","joyful expression","calm face",
              "neutral expression","relaxed face"],
        "b": ["ahegao","mind break","mind blown","eyes rolling","rolled back eyes",
              "tongue hanging out","drooling uncontrollably"],
        "prefer": "b",
    },
    # ---- 意識あり vs 意識なし ----
    {
        "name": "conscious_vs_unconscious",
        "a": ["awake","conscious","aware","alert","looking at viewer"],
        "b": ["unconscious","passed out","fainted","limp body","eyes closed unconscious",
              "completely unconscious","knocked out"],
        "prefer": "b",
    },
    # ---- no sexual activity vs 性行為タグ ----
    {
        "name": "nosex_vs_sex",
        "a": ["no sexual activity","non-sexual","sfw","no explicit","safe for work"],
        "b": ["penetration","insertion visible","sex","intercourse","fucking",
              "vaginal sex","anal sex","oral sex","blowjob","handjob"],
        "prefer": "b",
    },
    # ---- 平静/落ち着き vs 激しい表情 ----
    {
        "name": "calm_vs_intense",
        "a": ["calm face","neutral expression","stoic","expressionless","blank face",
              "resting face","composed"],
        "b": ["ahegao","orgasm face","screaming","crying loudly","terrified",
              "pained expression","euphoric","overwhelmed"],
        "prefer": "b",
    },
]

# ===== rewrites =====
# a群とb群が同居した時、両方削除して replace リストに置換

REWRITES = [
    # 苦痛+瞳孔散大 → 痛み表情として統合
    {
        "name": "pain_plus_dilated",
        "a": ["pained expression","grimacing","suffering","wincing"],
        "b": ["dilated pupils"],
        "replace": ["(pained expression:1.5)","(tightly shut eyes:1.4)",
                    "(clenched teeth:1.4)","(dilated pupils:1.5)","(pale face:1.3)"],
    },
]

# ===== メイン処理 =====
# real.json に書き込む
with open(r'C:\AI\ComfyUI\quality_rules\real.json', encoding='utf-8') as f:
    real = json.load(f)

real['dedupe_groups'] = DEDUPE_GROUPS
real['conflicts']     = CONFLICTS
real['rewrites']      = REWRITES

# conflict_neg: conflicts発火時にネガへ追加するタグ
real['conflict_neg'] = [
    "(contradictory outfit state:1.5)",
    "(inconsistent clothing:1.5)",
]

with open(r'C:\AI\ComfyUI\quality_rules\real.json', 'w', encoding='utf-8') as f:
    json.dump(real, f, ensure_ascii=False, indent=2)

# _common.json にも同じ dedupe_groups / conflicts を入れる（anime WFにも適用）
with open(r'C:\AI\ComfyUI\quality_rules\_common.json', encoding='utf-8') as f:
    common = json.load(f)

# _common は全WF共通: 人数・単一頭部・解剖・着衣矛盾・顔矛盾だけ入れる
COMMON_DEDUPE = [g for g in DEDUPE_GROUPS if g['name'] in (
    'people_count','solo_emphasis','single_head','anatomically_correct',
    'quality_boost','sharpness','photo_realism','camera_type','raw_photo',
    'cute_appeal','expression_consistency','drool_type','eye_state',
)]
COMMON_CONFLICTS = [c for c in CONFLICTS if c['name'] in (
    'nude_vs_clothed','topless_vs_top_on','pantless_vs_panty',
    'expression_smile_vs_pain','expression_smile_vs_ahegao',
    'conscious_vs_unconscious','calm_vs_intense','nosex_vs_sex',
)]

# rulesサブキーに格納（_common.jsonの構造に合わせる）
if 'rules' not in common:
    common['rules'] = {}
common['rules']['dedupe_groups'] = COMMON_DEDUPE
common['rules']['conflicts']     = COMMON_CONFLICTS

with open(r'C:\AI\ComfyUI\quality_rules\_common.json', 'w', encoding='utf-8') as f:
    json.dump(common, f, ensure_ascii=False, indent=2)

print(f'real.json:')
print(f'  dedupe_groups: {len(DEDUPE_GROUPS)} groups')
print(f'  conflicts:     {len(CONFLICTS)} rules')
print(f'  rewrites:      {len(REWRITES)} rules')
print(f'_common.json:')
print(f'  dedupe_groups: {len(COMMON_DEDUPE)} groups')
print(f'  conflicts:     {len(COMMON_CONFLICTS)} rules')
print('DONE')
