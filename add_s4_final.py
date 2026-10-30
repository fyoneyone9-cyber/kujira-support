# -*- coding: utf-8 -*-
import sys, re, json, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8')

html_path = r'C:\AI\ComfyUI\dashboard.html'
json_path = r'C:\AI\ComfyUI\outfit_sets.json'

bak = html_path + '.bak_s4_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy2(html_path, bak)
print(f'Backup: {bak}')

S4_KEY = 'S0255'

# 30シーン（ASCII safe）
scenes = [
    ("01-meat-slave",   "(collar:1.8),(kneeling:1.9),(vacant expression:1.9),(penetration:1.7),(ahegao:1.6),(broken will:1.8),(tears streaming:1.6),(full nude:1.7)"),
    ("02-morning-duty", "(waking up:1.5),(collar:1.8),(lying on back:1.7),(penetration:1.8),(blank stare:1.9),(no resistance:1.9),(cum inside:1.7),(mindbroken:1.8)"),
    ("03-meal-service", "(sitting:1.5),(penetration from behind:1.8),(eating:1.4),(expressionless:1.9),(vacant eyes:1.8),(collar:1.7),(drooling:1.5),(mindbroken:1.7)"),
    ("04-mirror",       "(standing:1.5),(looking in mirror:1.6),(full nude:1.8),(tattoos:1.7),(piercings:1.8),(collar:1.8),(empty eyes:1.9),(brand mark:1.8)"),
    ("05-multi-serve",  "(kneeling:1.7),(oral sex:1.7),(penetration:1.8),(double penetration:1.8),(ahegao:1.7),(mindbroken:1.9),(collar:1.8),(tears:1.6)"),
    ("06-public-crawl", "(on all fours:1.9),(collar with leash:2.0),(being led by leash:1.9),(outdoor:1.5),(public humiliation:1.8),(vacant expression:1.9),(fully degraded:1.8),(mindbroken:1.8)"),
    ("07-leash-walk",   "(collar with leash:2.0),(being led by leash:1.9),(walking on all fours:1.9),(outdoor:1.6),(blank stare:1.9),(nude:1.7),(degraded:1.8),(broken spirit:1.9)"),
    ("08-display",      "(bound:1.9),(spread eagle:1.8),(restrained:1.8),(on display:1.8),(nude:1.8),(vacant eyes:1.9),(collar:1.8),(piercings:1.8),(exhibition:1.7)"),
    ("09-compared",     "(standing at attention:1.7),(inspected:1.7),(collar:1.8),(nude:1.7),(blank expression:1.9),(submissive:1.8),(mindbroken:1.7),(degraded:1.8)"),
    ("10-auction",      "(kneeling:1.8),(collar:1.9),(auction:1.7),(nude:1.7),(eyes unfocused:1.9),(passive:1.8),(brand mark:1.9),(broken will:1.9)"),
    ("11-piercing",     "(lying still:1.7),(new piercings:1.8),(no expression:1.9),(collar:1.8),(body modification:1.9),(submissive:1.8),(tears:1.5),(accepting:1.8)"),
    ("12-tattoo",       "(lying flat:1.7),(new tattoo:1.8),(blank stare:1.9),(collar:1.8),(ownership mark:1.9),(body modification:1.9),(resigned:1.8),(mindbroken:1.7)"),
    ("13-lactation",    "(kneeling:1.6),(nipple sucking:1.8),(forced lactation:1.7),(blank expression:1.9),(collar:1.8),(drooling:1.5),(mindbroken:1.8),(tears:1.5)"),
    ("14-insertion",    "(standing:1.5),(insertion:1.8),(forced:1.7),(vacant eyes:1.9),(collar:1.8),(full nude:1.7),(mindbroken:1.8),(resigned:1.9)"),
    ("15-electric",     "(bound:1.8),(electric play:1.7),(ahegao:1.8),(collar:1.8),(tears streaming:1.7),(mindbroken:1.9),(forced pleasure:1.8),(vacant:1.9)"),
    ("16-scream",       "(kneeling:1.8),(ecstasy expression:1.8),(penetration:1.8),(ahegao:1.9),(drooling:1.7),(mindbroken:1.9),(collar:1.8),(broken:1.9)"),
    ("17-slave-words",  "(kneeling:1.9),(submissive pose:1.8),(collar:1.9),(blank expression:1.8),(slave:1.9),(mindbroken:1.8),(degraded:1.7),(resigned:1.9)"),
    ("18-forced-mast",  "(self touching:1.8),(forced masturbation:1.7),(blank stare:1.9),(collar:1.8),(ahegao:1.7),(mindbroken:1.8),(tears:1.5),(vacant:1.9)"),
    ("19-multi-orgasm", "(orgasm:1.8),(multiple orgasms:1.7),(ahegao:1.9),(collar:1.8),(tears streaming:1.7),(mindbroken:1.9),(drooling:1.7),(broken:1.9)"),
    ("20-no-identity",  "(kneeling:1.9),(vacant stare:2.0),(collar:1.9),(nude:1.8),(slave number:1.8),(no identity:1.9),(mindbroken:2.0),(broken spirit:1.9)"),
    ("21-exhibit",      "(posed:1.8),(nude:1.8),(collar:1.9),(vacant eyes:1.9),(on display:1.8),(restrained:1.7),(piercings:1.8),(mindbroken:1.8)"),
    ("22-group-serve",  "(group service:1.8),(oral:1.7),(penetration:1.8),(ahegao:1.8),(collar:1.8),(mindbroken:1.9),(tears:1.6),(degraded:1.8)"),
    ("23-recorded",     "(recorded:1.6),(camera:1.5),(nude:1.8),(collar:1.8),(blank expression:1.9),(submissive pose:1.8),(mindbroken:1.8),(degraded:1.7)"),
    ("24-outdoor-nude", "(outdoor:1.6),(nude:1.8),(collar:1.8),(vacant eyes:1.8),(crouching:1.6),(degraded:1.9),(mindbroken:1.8),(public shame:1.7)"),
    ("25-bestial",      "(on all fours:1.9),(degraded:1.9),(collar:1.9),(vacant expression:1.9),(mindbroken:2.0),(broken will:1.9),(tears:1.6),(resigned:1.9)"),
    ("26-broken-smile", "(broken smile:1.9),(penetration:1.8),(ahegao:1.8),(collar:1.9),(mindbroken:2.0),(tears:1.6),(drooling:1.7),(insane expression:1.8)"),
    ("27-pleasure-add", "(penetration:1.9),(full nude:1.8),(ahegao:1.9),(collar:1.8),(mindbroken:1.9),(addicted to pleasure:1.8),(drooling:1.7),(broken:1.9)"),
    ("28-waiting",      "(kneeling:1.9),(waiting:1.7),(collar:1.9),(vacant expression:1.8),(nude:1.7),(mindbroken:1.8),(submissive:1.9),(dependent:1.8)"),
    ("29-pledge",       "(kneeling:1.9),(submissive:1.9),(collar:1.9),(eyes unfocused:1.9),(mindbroken:2.0),(slave:1.9),(broken spirit:1.9),(conditioning:1.8)"),
    ("30-eternal-hell", "(lying broken:1.8),(penetration:1.8),(ahegao:1.9),(collar:1.9),(mindbroken:2.0),(tears:1.7),(drooling:1.7),(eternal suffering:1.8)"),
]

labels_jp = [
    "01\u3010\u8089\u4fbf\u5668\u5ba3\u8a00\u3011\u4e3b\u306b\u8089\u4fbf\u5668\u3068\u547c\u3070\u308c\u308b",
    "02\u3010\u6bce\u671d\u306e\u7fa9\u52d9\u3011\u76ee\u899a\u3081\u3068\u540c\u6642\u306b\u5949\u4ed5",
    "03\u3010\u98df\u4e8b\u4e2d\u306e\u5949\u4ed5\u3011\u98df\u4e8b\u3057\u306a\u304c\u3089\u633f\u5165\u3055\u308c\u308b",
    "04\u3010\u6539\u9020\u5f8c\u306e\u93e1\u3011\u81ea\u5206\u306e\u59ff\u306b\u7121\u8868\u60c5\u3067\u898b\u3064\u3081\u308b",
    "05\u3010\u8907\u6570\u540c\u6642\u5949\u4ed5\u3011\u8907\u6570\u76f8\u624b\u306b\u540c\u6642\u5949\u4ed5",
    "06\u3010\u516c\u8846\u306e\u9762\u524d\u3067\u9019\u3044\u3064\u304f\u3070\u308b\u3011\u5c4b\u5916\u3067\u547d\u4ee4\u306b\u5f93\u3046",
    "07\u3010\u9996\u8f2a\u30ea\u30fc\u30c9\u3067\u6563\u6b69\u3011\u5916\u3092\u5f15\u304d\u56de\u3055\u308c\u308b",
    "08\u3010\u5c55\u793a\u53f0\u306b\u7e1b\u3089\u308c\u308b\u3011\u98fe\u308a\u7269\u3068\u3057\u3066\u56fa\u5b9a\u3055\u308c\u308b",
    "09\u3010\u4ed6\u306e\u5974\u96b7\u3068\u6bd4\u3079\u3089\u308c\u308b\u3011\u54c1\u5b9a\u3081\u3055\u308c\u308b",
    "10\u3010\u58f2\u8cb7\u3055\u308c\u308b\u77ac\u9593\u3011\u7af6\u58f2\u306b\u304b\u3051\u3089\u308c\u308b",
    "11\u3010\u8ffd\u52a0\u30d4\u30a2\u30b9\u65bd\u8853\u3011\u65b0\u305f\u306a\u30d4\u30a2\u30b9\u3092\u65bd\u3055\u308c\u308b",
    "12\u3010\u523a\u9752\u8ffd\u52a0\u3011\u65b0\u305f\u306a\u70d9\u5370\u3092\u5c01\u5370\u3055\u308c\u308b",
    "13\u3010\u5f37\u5236\u6388\u4e73\u8abf\u6559\u3011\u4e73\u9996\u3092\u5438\u308f\u308c\u7d9a\u3051\u308b",
    "14\u3010\u819f\u5185\u7570\u7269\u633f\u5165\u3011\u547d\u4ee4\u3067\u7570\u7269\u3092\u633f\u308c\u305f\u307e\u307e\u751f\u6d3b",
    "15\u3010\u96fb\u6c17\u8ca6\u3081\u8abf\u6559\u3011\u96fb\u6d41\u3067\u5febv\u611f\u3092\u5f37\u5236\u3055\u308c\u308b",
    "16\u3010\u4e3b\u306e\u540d\u524d\u3092\u53eb\u3076\u3011\u53cd\u5c04\u7684\u306b\u53eb\u3076\u307e\u3067\u8abf\u6559",
    "17\u3010\u81ea\u5206\u304c\u5974\u96b7\u3060\u3068\u8a00\u308f\u3055\u308c\u308b\u3011\u8a00\u8449\u306e\u670d\u5f93",
    "18\u3010\u547d\u4ee4\u3067\u81ea\u6170\u3055\u305b\u3089\u308c\u308b\u3011\u5f37\u5236\u30aa\u30ca\u30cb\u30fc",
    "19\u3010\u9023\u7d9a\u7d76\u9802\u306e\u679c\u3066\u3011\u4f55\u5ea6\u3082\u5f37\u5236\u7d76\u9802\u3055\u305b\u3089\u308c\u308b",
    "20\u3010\u5b8c\u5168\u306a\u4eba\u683c\u6d88\u53bb\u3011\u540d\u524d\u3082\u5fd8\u308c\u756a\u53f7\u3067\u547c\u3070\u308c\u308b",
    "21\u3010\u751f\u4f53\u5c55\u793a\u54c1\u3068\u3057\u3066\u98fe\u3089\u308c\u308b\u3011\u90e8\u5c4b\u306e\u88c5\u98fe\u306b\u306a\u308b",
    "22\u3010\u30b0\u30eb\u30fc\u30d7\u5949\u4ed5\u3011\u8907\u6570\u4eba\u306e\u5ba2\u306b\u5949\u4ed5\u3055\u305b\u3089\u308c\u308b",
    "23\u3010\u6620\u50cf\u8a18\u9332\u3055\u308c\u308b\u3011\u8abf\u6559\u3092\u9332\u753b\u3055\u308c\u308b",
    "24\u3010\u7f70\u3068\u3057\u3066\u5916\u306b\u51fa\u3055\u308c\u308b\u3011\u88f8\u3067\u5916\u306b\u653e\u308a\u51fa\u3055\u308c\u308b",
    "25\u3010\u5947\u5f62\u8abf\u6559\u3011\u975e\u4eba\u9053\u7684\u547d\u4ee4\u306b\u670d\u5f93",
    "26\u3010\u8133\u304c\u58ca\u308c\u305f\u7b11\u9854\u3011\u58ca\u308c\u305f\u7b11\u9854\u3067\u5949\u4ed5\u3059\u308b",
    "27\u3010\u5feb\u697d\u306b\u6eba\u308c\u305f\u4f53\u3011\u6297\u3046\u3053\u3068\u306e\u3067\u304d\u306a\u3044\u4f53\u306b\u306a\u3063\u305f",
    "28\u3010\u4e3b\u3092\u5f85\u3061\u308f\u3073\u308b\u591c\u3011\u547d\u4ee4\u304c\u306a\u3044\u3068\u4e0d\u5b89\u306b\u306a\u308b",
    "29\u3010\u5b8c\u5168\u670d\u5f93\u306e\u8a93\u3044\u3011\u81ea\u3089\u306e\u610f\u5fd7\u3067\u5f93\u3046\u3068\u9322\u899a\u3059\u308b",
    "30\u3010\u7d42\u308f\u308a\u306a\u304d\u5730\u7344\u306e\u65e5\u5e38\u3011\u3053\u308c\u304c\u6c38\u9060\u306b\u7d9a\u304f",
]

S4_OUTFITS = [{"label": labels_jp[i], "prompt": scenes[i][1]} for i in range(30)]

with open(json_path,'r',encoding='utf-8') as f:
    d = json.load(f)
d[S4_KEY] = S4_OUTFITS
with open(json_path,'w',encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print(f'outfit_sets.json: {S4_KEY} = {len(S4_OUTFITS)} outfits OK')

# dashboard.html
with open(html_path,'r',encoding='utf-8') as f:
    c = f.read()

S4_CHARS = [
    ("char_kaizo_nichijou4_jk_A",
     "\U0001f3e0\U0001f489\u2620\u72c2\u6c17\u6539\u9020S4 JK-A\uff08\u9ed2\u9aea\uff09",
     "16 years old,teen,black straight long hair,(teen:1.4),nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),insane,completely destroyed mind,subhuman existence"),
    ("char_kaizo_nichijou4_jk_B",
     "\U0001f3e0\U0001f489\u2620\u72c2\u6c17\u6539\u9020S4 JK-B\uff08\u8336\u9aea\uff09",
     "16 years old,teen,brown wavy long hair,(teen:1.4),nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),insane,completely destroyed mind,subhuman existence"),
    ("char_kaizo_nichijou4_jk_C",
     "\U0001f3e0\U0001f489\u2620\u72c2\u6c17\u6539\u9020S4 JK-C\uff08\u91d1\u9aea\uff09",
     "16 years old,teen,blonde short hair,(teen:1.4),nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),insane,completely destroyed mind,subhuman existence"),
    ("char_kaizo_nichijou4_jc_A",
     "\U0001f3e0\U0001f489\u2620\u72c2\u6c17\u6539\u9020S4 JC-A\uff08\u9ed2\u9aea\uff09",
     "13 years old,slim,black straight long hair,(teen:1.5),(youthful face:1.5),nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),insane,completely destroyed mind"),
    ("char_kaizo_nichijou4_jc_B",
     "\U0001f3e0\U0001f489\u2620\u72c2\u6c17\u6539\u9020S4 JC-B\uff08\u8336\u9aea\uff09",
     "13 years old,slim,brown wavy hair,(teen:1.5),(youthful face:1.5),nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),insane,completely destroyed mind"),
    ("char_kaizo_nichijou4_jc_C",
     "\U0001f3e0\U0001f489\u2620\u72c2\u6c17\u6539\u9020S4 JC-C\uff08\u9280\u9aea\uff09",
     "13 years old,slim,silver white hair,(teen:1.5),(youthful face:1.5),nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),insane,completely destroyed mind"),
    ("char_kaizo_nichijou4_js_A",
     "\U0001f3e0\U0001f489\u2620\u72c2\u6c17\u6539\u9020S4 JS-A\uff08\u9ed2\u9aea\uff09",
     "9 years old,slender body,black straight hair,(young child:1.7),(child face:1.6),nipple piercings,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),insane,completely destroyed mind"),
    ("char_kaizo_nichijou4_aerith",
     "\U0001f3e0\U0001f489\u2620\u72c2\u6c17\u6539\u9020S4 \u30a8\u30a2\u30ea\u30b9",
     "Aerith Gainsborough,Final Fantasy VII,long brown hair with ribbon,green eyes,slender,22 years old,nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),(aerith gainsborough:1.9),(final fantasy:1.8),(ff7:1.8),insane,completely destroyed mind"),
    ("char_kaizo_nichijou4_tifa",
     "\U0001f3e0\U0001f489\u2620\u72c2\u6c17\u6539\u9020S4 \u30c6\u30a3\u30d5\u30a1",
     "Tifa Lockhart,Final Fantasy VII,long black hair dolphin-tail split,red eyes,athletic,20 years old,nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),(tifa lockhart:1.9),(final fantasy:1.8),(ff7:1.8),insane,completely destroyed mind"),
]

push_block = "\n// ===== [S4] \u72c2\u6c17\u6539\u9020S4 9\u4f53\uff082026-10-22\u8ffd\u52a0\uff09=====\n"
for cid, lbl, prmpt in S4_CHARS:
    push_block += f"window.CHAR_TEMPLATES.female.push({{id:'{cid}',label:'{lbl}',age:'unknown',prompt:'{prmpt}',outfits_ref:'{S4_KEY}'}});\n"
push_block += "// ===== /[S4] =====\n"

s5_first = "window.CHAR_TEMPLATES.female.push({id:'char_kaizo_nichijou5_jk_A'"
if s5_first in c:
    c = c.replace(s5_first, push_block + s5_first, 1)
    print('S4 chars inserted')

gd5 = "{key:'kaizo_nichijou5'"
if gd5 in c:
    c = c.replace(gd5, "{key:'kaizo_nichijou4',label:'\U0001f3e0\U0001f489\u2620\u72c2\u6c17\u6539\u9020S4',fn:id => /^char_kaizo_nichijou4_/.test(id)},\n" + gd5, 1)
    print('CHAR_GROUP_DEFS added')

cat5 = "{ key:'kaizo_nichijou5'"
if cat5 in c:
    c = c.replace(cat5, "{ key:'kaizo_nichijou4', label:'\U0001f3e0\U0001f489\u2620\u72c2\u6c17\u6539\u9020S4', match: id => /^char_kaizo_nichijou4_/.test(id) },\n  " + cat5, 1)
    print('CHAR_CATEGORIES added')

c = re.sub(r"('kaizo_nichijou5')", r"'kaizo_nichijou4', \1", c, count=1)
print('CHAR_CATEGORY_GROUPS added')

genre_label = '\U0001f489 \u6539\u9020\u30fb\u6d17\u8133'
c = re.sub(
    r"('kaizo_nichijou5':'[^']*')",
    lambda m: f"'kaizo_nichijou4':'{genre_label}', " + m.group(1),
    c, count=1
)
print('_GP_BIG_GENRE_MAP added')

m = re.search(r"name=['\"]version['\"] content=['\"](\d+)['\"]", c)
if m:
    ov = m.group(1); nv = str(int(ov)+1)
    c = c.replace(f'content="{ov}"', f'content="{nv}"', 1)
    print(f'Version: {ov} -> {nv}')

with open(html_path,'w',encoding='utf-8') as f:
    f.write(c)
print('Saved.')

# JS構文チェック（test_map.jsを更新して確認）
import subprocess
r = subprocess.run(['node', '--check', html_path], capture_output=True, text=True, timeout=30)
if r.returncode == 0:
    print('JS syntax: OK')
else:
    print('JS ERROR:', r.stderr[:400])
