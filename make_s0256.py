import json, sys
sys.stdout.reconfigure(encoding='utf-8')

S0256 = [
    # 01-05: 肉体改造・焼印系（S4より過激な施術）
    {"label": "01【乳首焼印調教】焼き鏝で所有者の印を刻む",
     "prompt": "(branding iron:1.8),(nipple brand:1.7),(slave mark:2.0),(lying restrained:1.8),(screaming:1.0),(mindbroken:1.9),(collar:1.8),(full nude:1.8),(tears:1.6),(burn mark on nipple:1.7)"},
    {"label": "02【膣縫合施術】外科的改造で閉じられる",
     "prompt": "(surgical restraint:1.7),(medical table:1.6),(speculum:1.5),(collar:1.8),(blank stare:2.0),(mindbroken:1.9),(nude:1.8),(legs spread:1.7),(clinical scene:1.5),(no expression:2.0)"},
    {"label": "03【眼球に所有者名を刻む幻想】眼の奥まで改造される",
     "prompt": "(staring blankly:2.0),(hollow eyes:2.0),(collar:1.8),(nude:1.8),(mindbroken:2.0),(ownership marks all over body:1.8),(brand marks:1.9),(kneeling:1.7),(completely broken:2.0),(slave:1.8)"},
    {"label": "04【骨格レベルの服従訓練】体が命令を覚える",
     "prompt": "(stress position:1.8),(restrained kneeling:1.9),(collar:1.9),(nude:1.8),(trembling:1.6),(mindbroken:1.9),(tears streaming:1.5),(vacant eyes:2.0),(forced posture:1.8),(degraded:1.9)"},
    {"label": "05【全身タトゥー完成】もはや芸術品として扱われる",
     "prompt": "(full body tattoos:2.0),(ownership text tattooed:1.9),(collar:1.8),(standing:1.5),(displayed:1.7),(blank expression:2.0),(mindbroken:1.9),(nude:1.8),(slave number tattoo:1.8),(brand marks:1.8)"},

    # 06-10: 排泄・浣腸・屈辱系
    {"label": "06【公開排泄命令】人前でさせられる極限の屈辱",
     "prompt": "(squatting:1.8),(public humiliation:1.9),(collar:1.8),(nude:1.8),(degraded:2.0),(blank stare:1.9),(mindbroken:1.9),(tears:1.5),(forced humiliation:1.8),(vacant eyes:1.9)"},
    {"label": "07【浣腸調教】反論できない体にされる",
     "prompt": "(on all fours:1.9),(restrained:1.8),(collar:1.9),(nude:1.8),(degraded:1.9),(mindbroken:1.9),(ahegao:1.5),(tears:1.6),(trembling:1.5),(completely humiliated:1.9)"},
    {"label": "08【足舐め奉仕命令】床を這って足を舐める",
     "prompt": "(prostrating:1.9),(on floor:1.8),(licking feet:1.7),(collar with leash:1.9),(nude:1.8),(mindbroken:1.9),(degraded:2.0),(blank expression:1.9),(submissive:2.0),(forehead on floor:1.8)"},
    {"label": "09【食器なしの食事命令】犬のように床から食べる",
     "prompt": "(on all fours:1.9),(eating from floor:1.7),(collar:1.9),(nude:1.8),(degraded:2.0),(mindbroken:1.9),(blank stare:1.9),(completely broken:2.0),(pet behavior:1.8),(no dignity:1.9)"},
    {"label": "10【鎖で繋がれた部屋飼い】家具として生活させられる",
     "prompt": "(chained to wall:1.9),(kneeling:1.8),(collar with chain:2.0),(nude:1.8),(mindbroken:2.0),(vacant eyes:2.0),(degraded:1.9),(pet:1.7),(no furniture rights:1.8),(completely broken:2.0)"},

    # 11-15: 繁殖・生体実験系
    {"label": "11【繁殖用として管理される】子を産む道具として扱われる",
     "prompt": "(restrained on breeding table:1.8),(collar:1.9),(nude:1.8),(mindbroken:2.0),(vacant eyes:2.0),(penetration:1.8),(degraded:1.9),(blank expression:2.0),(breeding:1.7),(completely broken:1.9)"},
    {"label": "12【薬物注射で発情させられる】意志とは関係なく体が反応する",
     "prompt": "(syringe:1.5),(drug injection:1.4),(flushed skin:1.8),(ahegao:1.9),(collar:1.8),(nude:1.8),(mindbroken:1.9),(addicted:1.8),(self touching:1.6),(completely broken:1.9)"},
    {"label": "13【催眠音声で洗脳継続】眠っていても調教が続く",
     "prompt": "(sleeping:1.5),(headphones:1.4),(collar:1.8),(nude:1.8),(mindbroken:2.0),(vacant expression:2.0),(brainwashed:1.9),(completely conditioned:1.9),(blank stare:2.0),(no resistance:1.9)"},
    {"label": "14【性器に鍵をつけられる】主の許可なく快楽を得られない",
     "prompt": "(chastity device:1.7),(collar:1.8),(nude:1.8),(mindbroken:1.9),(kneeling:1.8),(degraded:1.9),(vacant eyes:2.0),(waiting:1.6),(controlled:1.9),(completely broken:2.0)"},
    {"label": "15【子宮に所有者の名前を彫られる幻想】最深部まで改造",
     "prompt": "(lying spread:1.8),(medical restraint:1.7),(collar:1.8),(nude:1.8),(mindbroken:2.0),(vacant stare:2.0),(completely broken:2.0),(ownership brand:1.9),(degraded:1.9),(no will:2.0)"},

    # 16-20: 公開・展示・競売系（S4より大規模）
    {"label": "16【公開競売】複数の買い手の前で競り落とされる",
     "prompt": "(auction stage:1.7),(multiple viewers:1.5),(collar:1.9),(nude:1.8),(kneeling:1.8),(mindbroken:2.0),(vacant eyes:2.0),(degraded:1.9),(inspected:1.8),(completely broken:2.0)"},
    {"label": "17【ショーケースに入れられる】商品として陳列",
     "prompt": "(in glass case:1.7),(displayed:1.9),(collar:1.8),(nude:1.8),(mindbroken:2.0),(kneeling:1.8),(vacant stare:2.0),(degraded:1.9),(object:1.8),(completely broken:2.0)"},
    {"label": "18【公開性処理】観客の前で使われる",
     "prompt": "(public:1.7),(audience watching:1.5),(penetration:1.8),(collar:1.9),(nude:1.8),(ahegao:1.9),(mindbroken:2.0),(tears:1.5),(degraded:1.9),(completely broken:1.9)"},
    {"label": "19【写真集撮影強制】メディアに記録される",
     "prompt": "(photoshoot:1.6),(multiple cameras:1.4),(nude:1.8),(collar:1.8),(forced pose:1.7),(mindbroken:2.0),(blank expression:2.0),(degraded:1.9),(exploited:1.8),(completely broken:1.9)"},
    {"label": "20【SNS配信される】全世界に晒される",
     "prompt": "(livestream:1.5),(camera recording:1.6),(penetration:1.8),(collar:1.8),(nude:1.8),(ahegao:1.9),(mindbroken:2.0),(tears:1.5),(public humiliation:1.8),(degraded:1.9)"},

    # 21-25: 輪姦・多人数系（S4より人数増）
    {"label": "21【三穴同時使用】全ての穴を同時に犯される",
     "prompt": "(triple penetration:1.9),(airtight:1.8),(collar:1.9),(ahegao:2.0),(mindbroken:2.0),(tears:1.6),(drooling:1.7),(cum:1.5),(completely broken:2.0),(degraded:1.9)"},
    {"label": "22【白濁まみれのアヘ顔】全身を汚される",
     "prompt": "(covered in cum:1.9),(cum on face:1.8),(cum on body:1.8),(ahegao:2.0),(collar:1.8),(nude:1.8),(mindbroken:2.0),(tears:1.5),(drooling:1.7),(completely broken:2.0)"},
    {"label": "23【延々と続く輪姦】何人目か数えられない",
     "prompt": "(gangbang:1.9),(multiple penetration:1.8),(collar:1.9),(ahegao:2.0),(mindbroken:2.0),(tears:1.6),(drooling:1.7),(cum:1.5),(degraded:1.9),(completely broken:2.0)"},
    {"label": "24【人体椅子にされる】家具として使用される",
     "prompt": "(used as furniture:1.8),(penetration while kneeling:1.8),(collar:1.9),(nude:1.8),(mindbroken:2.0),(blank stare:2.0),(degraded:1.9),(completely broken:2.0),(no will:2.0),(objectified:1.9)"},
    {"label": "25【精液プールに沈められる】完全汚辱",
     "prompt": "(covered completely in cum:2.0),(ahegao:2.0),(collar:1.9),(nude:1.8),(mindbroken:2.0),(completely broken:2.0),(degraded:1.9),(tears:1.5),(drooling:1.7),(blank expression:1.9)"},

    # 26-30: 人格消去・廃人・永久堕落
    {"label": "26【名前も記憶も消える】誰だったか覚えていない",
     "prompt": "(kneeling:1.9),(hollow eyes:2.0),(collar:1.9),(nude:1.8),(mindbroken:2.0),(completely broken:2.0),(vacant stare:2.0),(no memory:1.9),(degraded:1.9),(only obedience remains:1.9)"},
    {"label": "27【廃人として倉庫に保管される】使い終わって放置",
     "prompt": "(lying discarded:1.8),(storage room:1.5),(collar:1.9),(nude:1.8),(mindbroken:2.0),(blank stare:2.0),(completely broken:2.0),(abandoned:1.7),(cum leaking:1.6),(no will:2.0)"},
    {"label": "28【死んだ目で微笑む】魂が完全に消えた",
     "prompt": "(dead eyes:2.0),(vacant smile:1.9),(collar:1.9),(nude:1.8),(mindbroken:2.0),(completely broken:2.0),(kneeling:1.8),(degraded:1.9),(hollow:2.0),(no soul:1.9)"},
    {"label": "29【永遠の調教を受け入れた】これが自分だと思い込む",
     "prompt": "(kneeling:1.9),(blank smile:1.9),(collar:1.9),(nude:1.8),(penetration:1.8),(mindbroken:2.0),(ahegao:1.8),(completely broken:2.0),(accepts fate:1.9),(degraded:1.9)"},
    {"label": "30【完全な肉塊】人間ではなくなった",
     "prompt": "(lying broken:1.9),(multiple penetration:1.8),(collar:1.9),(ahegao:2.0),(mindbroken:2.0),(cum all over:1.8),(completely broken:2.0),(tears:1.5),(drooling:1.7),(degraded:1.9)"},
]

print(f"S0256: {len(S0256)}シーン")
for i, x in enumerate(S0256):
    print(f"  {i:02d}: {x['label']}")

# outfit_sets.json に追加
with open('C:/AI/ComfyUI/outfit_sets.json', encoding='utf-8') as f:
    d = json.load(f)

if 'S0256' in d:
    print("\n⚠️ S0256 already exists, overwriting")
d['S0256'] = S0256

with open('C:/AI/ComfyUI/outfit_sets.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)

print(f"\n✅ S0256 追加完了 (total keys: {len(d)})")
