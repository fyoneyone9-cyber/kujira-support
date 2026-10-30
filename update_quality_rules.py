import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\AI\ComfyUI\quality_rules\real.json', encoding='utf-8') as f:
    d = json.load(f)

# ===== weight_budget.keep: 圧縮対象外（部分一致） =====
WB_KEEP = [
    # 人数
    '1girl','solo','only one','one person','single',
    # 年齢数値
    'year old','years old','age ','cm','child height',
    # 外見年齢
    'teen','teenager','young teen','youthful','childlike','juvenile',
    'young face','teen face','immature','young girl','young woman',
    'little girl','small girl','petite girl','loli','lolita',
    'underage','minor','preteen','adolescent','prepubescent',
    # 体型全般
    'physique','body type','build','figure','frame',
    'slender','slim','thin','skinny','lean','lithe',
    'petite','small','tiny','compact','short',
    'athletic','toned','fit','muscular','stocky',
    'tall','height',
    'slender body','slim body','thin body','small body','tiny body',
    'petite body','lean body','athletic body','toned body',
    'small stature','short stature','small frame','small build',
    'flat chest','small breasts','medium breasts','large breasts',
    'huge breasts','gigantic breasts','enormous breasts','breast size',
    'h-cup','j-cup','f-cup','e-cup','d-cup','c-cup','b-cup',
    'breast implant','augmented',
    'narrow waist','wide hips','thin waist','slender waist','curvy',
    # 身体的特徴
    'black hair','blonde','brown hair','white hair','silver hair','red hair',
    'red eyes','blue eyes','green eyes','purple eyes','golden eyes',
    'long hair','short hair','twin tail','ponytail','braid','pigtail',
    'dolphin','ahoge','ribbon','hairpin','twintail',
    # 場所・背景（完全網羅）
    'room','indoor','outdoor',
    'background','setting','environment','location','scene','scenery',
    'dim ','dark ','dimly lit','poorly lit','low light','dim lighting',
    'bright','sunlit','daylight','night',
    'hospital','clinic','operating room','examination room','medical',
    'sterile room','sterile','surgery','laboratory','lab',
    'bedroom','bathroom','toilet','kitchen','living room','dining',
    'classroom','school','hallway','corridor','locker room',
    'office','workspace','conference',
    'alley','street','road','sidewalk','park','garden',
    'warehouse','basement','dungeon','cell','prison','cage',
    'rooftop','balcony','staircase',
    'hotel','inn','motel','apartment',
    'forest','woods','beach','pool','bath','onsen',
    'stage','studio','dressing room',
    'restraint room','examination table','operating table','medical table',
    'wall','floor','bed','chair','desk','table','couch','sofa',
    # 構図フレーミング
    'full body','full body shot','whole body','entire body',
    'upper body','upper body shot','bust shot','waist up',
    'lower body','lower half',
    'cowboy shot','medium shot','wide shot','long shot','extreme long shot',
    'close-up','close up','portrait','head shot','headshot','face shot',
    'head and shoulders','torso shot',
    'from front','frontal','straight on',
    'from side','side view','profile',
    'from behind','back view','rear view',
    'from above','high angle','bird eye',"bird's eye",
    'from below','low angle',"worm's eye",
    'eye level','eye-level',
    'dutch angle','tilted',
    'pov','point of view','first person','over shoulder',
    'looking at viewer','looking up','looking down','looking away',
    'framing','camera angle','camera distance','depth of field',
    # 姿勢・ポーズ
    'standing','sitting','lying','kneeling','crouching','squatting',
    'leaning','bending','bent over','all fours','on back','on stomach',
    'legs apart','legs together','legs up','spread legs',
    'arms up','arms behind','hands behind','hands bound',
    'restrained','bound','tied',
    # 照明・雰囲気
    'lighting','light ','shadow','ambient',
    'soft light','natural light','window light','moonlight','candlelight',
    'spotlight','backlight','rim light','side light',
    'warm','cool','cold','blue tint','warm tone',
    # シーン状況
    'alone','private','secret','hidden',
    'awake','asleep','unconscious','drugged','sedated',
    'restrained','bound','gagged','blindfolded','handcuffed',
    'naked','clothed','undressed','dressed',
]

d['weight_budget'] = {'keep': WB_KEEP}

# ===== pos_cap_immune: cap1.35クランプ除外（完全版） =====
BASE_IMMUNE = [
    'photorealistic','raw photo','realistic skin','detailed skin','skin pores',
    'subsurface','dslr','detailed face','sharp detailed eyes',
    '1girl','solo','child height','year old','cm','physique',
    'pubic','pubes','hairless','shaved pussy','bald pussy','smooth pubic',
    'no body hair','prepubescent genitalia','clitoris','clitoral','labia',
    'vulva','genital','intimate area','gynecological',
    'ring through','pierced','piercing','nipple','nipple ring','nipple piercing',
    'nipple rings','navel piercing','navel ring','clitoral ring','labia ring',
    'breast implants','f-cup',
    'unconscious','restrain','needle',
    'pleasure','orgasm','climax','ahegao','eyes rolling','tongue out',
    'tears','crying','teary','training','forced','reluctant','unwilling',
    'trembling','stimulation','tugged','brand mark','branded',
    'drool','saliva','panting','moaning','arched back','convuls',
    'fully clothed','clothing stays on','clothing intact','stays on',
    'covered by clothing','covered by shirt','hidden under clothing',
    'chest covered','lower body still clothed','wearing skirt','wearing panties',
    'skirt covering','fabric over',
    'medium shot','full body shot','close-up','waist up',
    'from above','from below','looking at viewer','pov','framing','camera angle',
]
ADD_IMMUNE = [
    # 体型
    'slender','slim','thin','skinny','lean','lithe','petite','compact',
    'athletic','toned','fit','muscular',
    'slender body','slim body','thin body','small body','tiny body',
    'petite body','lean body','athletic body','toned body',
    'small stature','short stature','small build','small frame',
    'narrow waist','slender waist','thin waist',
    'flat chest','small breasts','huge breasts','gigantic breasts','enormous breasts',
    'h-cup','j-cup','e-cup','d-cup','c-cup','b-cup','breast implant','augmented',
    # 外見年齢
    'teen','teenager','young teen','youthful','childlike','juvenile',
    'young face','teen face','immature','young girl','loli','lolita',
    'underage','preteen','adolescent','prepubescent',
    # 場所
    'dim room','dark room','dimly lit','low light',
    'hospital','clinic','operating room','examination room','sterile room',
    'medical','surgery','laboratory',
    'bedroom','bathroom','classroom','school','office','warehouse',
    'basement','dungeon','prison','cage','rooftop','alley','street','park',
    'hotel','apartment','room','indoor','outdoor',
    'examination table','operating table','medical table','restraint room',
    'bed','floor','wall','chair','desk','couch','sofa',
    # 構図
    'full body','upper body','lower body','whole body','entire body',
    'cowboy shot','wide shot','long shot','bust shot','head shot',
    'from front','from side','from behind','from above','from below',
    'eye level','eye-level','high angle','low angle','dutch angle',
    # 姿勢
    'standing','sitting','lying','kneeling','crouching','all fours',
    'on back','on stomach','legs up','legs apart','spread legs',
    'bent over','leaning','bending',
    # 照明
    'lighting','soft light','natural light','moonlight','candlelight',
    'warm tone','cool tone','blue tint',
    # キャラ特徴
    'red eyes','blue eyes','green eyes','purple eyes','golden eyes',
    'black hair','blonde','brown hair','white hair','silver hair','red hair',
    'long black hair','dolphin','twintail','twin tail','ponytail','braid',
    # シーン状況
    'drugged','sedated','bound','gagged','blindfolded','handcuffed',
    'alone','private','restrained',
]
all_immune = BASE_IMMUNE[:]
for x in ADD_IMMUNE:
    if x not in all_immune:
        all_immune.append(x)
d['pos_cap_immune'] = all_immune

with open(r'C:\AI\ComfyUI\quality_rules\real.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f'weight_budget.keep: {len(d["weight_budget"]["keep"])} items')
print(f'pos_cap_immune: {len(d["pos_cap_immune"])} items')
print('DONE')
