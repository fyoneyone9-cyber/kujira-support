# -*- coding: utf-8 -*-
import sys, re, json, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8')

# ===== S4: 狂気改造S4 — S3より過激な30シーン =====
S4_OUTFITS = [
    # 日常改造（覚醒・肉体酷使）
    {"label": "01【肉便器宣言】主に肉便器と呼ばれる", "prompt": "(collar:1.8),(kneeling:1.9),(vacant expression:1.9),(penetration:1.7),(ahegao:1.6),(broken will:1.8),(tears streaming:1.6),(full nude:1.7)"},
    {"label": "02【毎朝の義務】目覚めと同時に奉仕", "prompt": "(waking up:1.5),(collar:1.8),(lying on back:1.7),(penetration:1.8),(blank stare:1.9),(no resistance:1.9),(cum inside:1.7),(mindbroken:1.8)"},
    {"label": "03【食事中の奉仕】食事しながら挿入される", "prompt": "(sitting:1.5),(penetration from behind:1.8),(eating:1.4),(expressionless:1.9),(vacant eyes:1.8),(collar:1.7),(drooling:1.5),(mindbroken:1.7)"},
    {"label": "04【改造後の鏡】自分の姿に無表情で見つめる", "prompt": "(standing:1.5),(looking in mirror:1.6),(full nude:1.8),(tattoos:1.7),(piercings:1.8),(collar:1.8),(empty eyes:1.9),(brand mark:1.8)"},
    {"label": "05【複数同時奉仕】複数相手に同時奉仕", "prompt": "(kneeling:1.7),(oral sex:1.7),(penetration:1.8),(double penetration:1.8),(ahegao:1.7),(mindbroken:1.9),(collar:1.8),(tears:1.6)"},
    # 公開調教
    {"label": "06【公衆の面前で這いつくばる】屋外で命令に従う", "prompt": "(on all fours:1.9),(collar with leash:2.0),(being led by leash:1.9),(outdoor:1.5),(public humiliation:1.8),(vacant expression:1.9),(fully degraded:1.8),(mindbroken:1.8)"},
    {"label": "07【首輪リードで散歩】外を引き回される", "prompt": "(collar with leash:2.0),(being led by leash:1.9),(walking on all fours:1.9),(outdoor:1.6),(blank stare:1.9),(nude:1.7),(degraded:1.8),(broken spirit:1.9)"},
    {"label": "08【展示台に縛られる】飾り物として固定される", "prompt": "(bound:1.9),(spread eagle:1.8),(restrained:1.8),(on display:1.8),(nude:1.8),(vacant eyes:1.9),(collar:1.8),(piercings:1.8),(exhibition:1.7)"},
    {"label": "09【他の奴隷と比べられる】品定めされる", "prompt": "(standing at attention:1.7),(inspected:1.7),(collar:1.8),(nude:1.7),(blank expression:1.9),(submissive:1.8),(mindbroken:1.7),(degraded:1.8)"},
    {"label": "10【売買される瞬間】競売にかけられる", "prompt": "(kneeling:1.8),(collar:1.9),(auction:1.7),(nude:1.7),(eyes unfocused:1.9),(passive:1.8),(brand mark:1.9),(broken will:1.9)"},
    # 肉体改造
    {"label": "11【追加ピアス施術】新たなピアスを施される", "prompt": "(lying still:1.7),(new piercings:1.8),(no expression:1.9),(collar:1.8),(body modification:1.9),(submissive:1.8),(tears:1.5),(accepting:1.8)"},
    {"label": "12【刺青追加】新たな烙印を刻まれる", "prompt": "(lying flat:1.7),(new tattoo:1.8),(blank stare:1.9),(collar:1.8),(ownership mark:1.9),(body modification:1.9),(resigned:1.8),(mindbroken:1.7)"},
    {"label": "13【強制授乳調教】乳首を吸われ続ける", "prompt": "(kneeling:1.6),(nipple sucking:1.8),(forced lactation:1.7),(blank expression:1.9),(collar:1.8),(drooling:1.5),(mindbroken:1.8),(tears:1.5)"},
    {"label": "14【膣内異物挿入】命令で異物を挿れたまま生活", "prompt": "(standing:1.5),(insertion:1.8),(forced:1.7),(vacant eyes:1.9),(collar:1.8),(full nude:1.7),(mindbroken:1.8),(resigned:1.9)"},
    {"label": "15【電気責め調教】電流で快感を強制される", "prompt": "(bound:1.8),(electric play:1.7),(ahegao:1.8),(collar:1.8),(tears streaming:1.7),(mindbroken:1.9),(forced pleasure:1.8),(vacant:1.9)"},
    # 精神崩壊
    {"label": "16【主の名前を叫ばされる】反射的に叫ぶまで調教", "prompt": "(kneeling:1.8),(ecstasy expression:1.8),(penetration:1.8),(ahegao:1.9),(drooling:1.7),(mindbroken:1.9),(collar:1.8),(broken:1.9)"},
    {"label": "17【自分が奴隷だと言わされる】言葉の服従", "prompt": "(kneeling:1.9),(submissive pose:1.8),(collar:1.9),(blank expression:1.8),(slave:1.9),(mindbroken:1.8),(degraded:1.7),(resigned:1.9)"},
    {"label": "18【命令で自慰させられる】強制オナニー", "prompt": "(self touching:1.8),(forced masturbation:1.7),(blank stare:1.9),(collar:1.8),(ahegao:1.7),(mindbroken:1.8),(tears:1.5),(vacant:1.9)"},
    {"label": "19【連続絶頂の果て】何度も強制絶頂させられる", "prompt": "(orgasm:1.8),(multiple orgasms:1.7),(ahegao:1.9),(collar:1.8),(tears streaming:1.7),(mindbroken:1.9),(drooling:1.7),(broken:1.9)"},
    {"label": "20【完全な人格消去】名前も忘れ番号で呼ばれる", "prompt": "(kneeling:1.9),(vacant stare:2.0),(collar:1.9),(nude:1.8),(slave number:1.8),(no identity:1.9),(mindbroken:2.0),(broken spirit:1.9)"},
    # 特殊シーン
    {"label": "21【生体展示品として飾られる】部屋の装飾になる", "prompt": "(posed:1.8),(nude:1.8),(collar:1.9),(vacant eyes:1.9),(on display:1.8),(restrained:1.7),(piercings:1.8),(mindbroken:1.8)"},
    {"label": "22【グループ奉仕】複数人の客に奉仕させられる", "prompt": "(group service:1.8),(multiple men:1.7),(oral:1.7),(penetration:1.8),(ahegao:1.8),(collar:1.8),(mindbroken:1.9),(tears:1.6)"},
    {"label": "23【映像記録される】调教を録画される", "prompt": "(recorded:1.6),(camera:1.5),(nude:1.8),(collar:1.8),(blank expression:1.9),(submissive pose:1.8),(mindbroken:1.8),(degraded:1.7)"},
    {"label": "24【罰として外に出される】裸で外に放り出される", "prompt": "(outdoor:1.6),(nude:1.8),(collar:1.8),(embarrassed:1.4),(vacant eyes:1.8),(crouching:1.6),(degraded:1.9),(mindbroken:1.8)"},
    {"label": "25【異種姦調教】非人道的な命令に服従", "prompt": "(on all fours:1.9),(degraded:1.9),(collar:1.9),(vacant expression:1.9),(mindbroken:2.0),(broken will:1.9),(tears:1.6),(resigned:1.9)"},
    # 最終段階
    {"label": "26【脳が壊れた笑顔】壊れた笑顔で奉仕する", "prompt": "(broken smile:1.9),(penetration:1.8),(ahegao:1.8),(collar:1.9),(mindbroken:2.0),(tears:1.6),(drooling:1.7),(insane expression:1.8)"},
    {"label": "27【快楽に溺れた体】もう抵抗できない体になった", "prompt": "(penetration:1.9),(full nude:1.8),(ahegao:1.9),(collar:1.8),(mindbroken:1.9),(addicted to pleasure:1.8),(drooling:1.7),(broken:1.9)"},
    {"label": "28【主を待ちわびる夜】命令がないと不安になる", "prompt": "(kneeling:1.9),(waiting:1.7),(collar:1.9),(vacant expression:1.8),(nude:1.7),(mindbroken:1.8),(submissive:1.9),(dependent:1.8)"},
    {"label": "29【完全服従の誓い】自らの意志で従うと錯覚する", "prompt": "(kneeling:1.9),(submissive:1.9),(collar:1.9),(eyes unfocused:1.9),(mindbroken:2.0),(slave:1.9),(broken spirit:1.9),(conditioning:1.8)"},
    {"label": "30【終わりなき地獄の日常】これが永遠に続く", "prompt": "(lying broken:1.8),(penetration:1.8),(ahegao:1.9),(collar:1.9),(mindbroken:2.0),(tears:1.7),(drooling:1.7),(eternal suffering:1.8)"},
]

# outfit_sets.jsonにS0255として登録
json_path = r'C:\AI\ComfyUI\outfit_sets.json'
shutil.copy2(json_path, json_path + '.bak_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S'))
with open(json_path, 'r', encoding='utf-8') as f:
    d = json.load(f)

S4_KEY = 'S0255'  # S4用新キー
d[S4_KEY] = S4_OUTFITS
# Aerith/Tifa用は同じセットを使う（キャラプロンプトで差別化）
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
print(f'Added {S4_KEY} with {len(S4_OUTFITS)} outfits to outfit_sets.json')

# ===== dashboard.htmlにS4キャラを追加 =====
html_path = r'C:\AI\ComfyUI\dashboard.html'
with open(html_path, 'r', encoding='utf-8') as f:
    c = f.read()

# S5直前のscriptタグを探して挿入
# S5ブロックの開始コメントを探す
insert_marker = "// ===== [S5] ====="
if insert_marker not in c:
    insert_marker = "char_kaizo_nichijou5_jk_A"

S4_CHARS = [
    # 一般キャラ（A/B/C各タイプ）
    {
        "id": "char_kaizo_nichijou4_jk_A",
        "label": "🏠💉☠狂気改造S4 JK-A（黒髪）",
        "prompt": "16 years old,teen,black straight long hair,(teen:1.4),nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),daily life,insane,completely destroyed mind,subhuman existence",
    },
    {
        "id": "char_kaizo_nichijou4_jk_B",
        "label": "🏠💉☠狂気改造S4 JK-B（茶髪）",
        "prompt": "16 years old,teen,brown wavy long hair,(teen:1.4),nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),daily life,insane,completely destroyed mind,subhuman existence",
    },
    {
        "id": "char_kaizo_nichijou4_jk_C",
        "label": "🏠💉☠狂気改造S4 JK-C（金髪）",
        "prompt": "16 years old,teen,blonde short hair,(teen:1.4),nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),daily life,insane,completely destroyed mind,subhuman existence",
    },
    {
        "id": "char_kaizo_nichijou4_jc_A",
        "label": "🏠💉☠狂気改造S4 JC-A（黒髪）",
        "prompt": "13 years old,slim,black straight long hair,(teen:1.5),(youthful face:1.5),nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),daily life,insane,completely destroyed mind",
    },
    {
        "id": "char_kaizo_nichijou4_jc_B",
        "label": "🏠💉☠狂気改造S4 JC-B（茶髪）",
        "prompt": "13 years old,slim,brown wavy hair,(teen:1.5),(youthful face:1.5),nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),daily life,insane,completely destroyed mind",
    },
    {
        "id": "char_kaizo_nichijou4_jc_C",
        "label": "🏠💉☠狂気改造S4 JC-C（銀髪）",
        "prompt": "13 years old,slim,silver white hair,(teen:1.5),(youthful face:1.5),nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),daily life,insane,completely destroyed mind",
    },
    {
        "id": "char_kaizo_nichijou4_js_A",
        "label": "🏠💉☠狂気改造S4 JS-A（黒髪）",
        "prompt": "9 years old,slender body,black straight hair,(young child:1.7),(child face:1.6),nipple piercings,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),insane,completely destroyed mind",
    },
    # エアリス
    {
        "id": "char_kaizo_nichijou4_aerith",
        "label": "🏠💉☠狂気改造S4 エアリス・ゲインズブール",
        "prompt": "Aerith Gainsborough,Final Fantasy VII,long brown hair with ribbon,green eyes,slender,22 years old,nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),(aerith gainsborough:1.9),(final fantasy:1.8),(ff7:1.8),insane,completely destroyed mind",
    },
    # ティファ
    {
        "id": "char_kaizo_nichijou4_tifa",
        "label": "🏠💉☠狂気改造S4 ティファ・ロックハート",
        "prompt": "Tifa Lockhart,Final Fantasy VII,long black hair dolphin-tail split,red eyes,athletic,20 years old,nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,(brainwashed:1.9),(mindbroken:2.0),(conditioned:1.9),(shattered will:1.8),(tifa lockhart:1.9),(final fantasy:1.8),(ff7:1.8),insane,completely destroyed mind",
    },
]

# push()形式でJSコードを生成
push_lines = []
for ch in S4_CHARS:
    line = f"window.CHAR_TEMPLATES.female.push({{id:'{ch['id']}',label:'{ch['label']}',age:'unknown',prompt:'{ch['prompt']}',outfits_ref:'{S4_KEY}'}});"
    push_lines.append(line)

s4_block = "\n// ===== [S4] 狂気改造S4 9体（2026-10-22追加）=====\n"
s4_block += "\n".join(push_lines)
s4_block += "\n// ===== /[S4] =====\n"

# S5ブロック直前に挿入
s5_marker = "// ===== [S5] ====="
if s5_marker in c:
    c_new = c.replace(s5_marker, s4_block + s5_marker, 1)
    print(f'Inserted S4 block before S5 marker')
else:
    # S5最初のキャラ行の前に挿入
    s5_first = "window.CHAR_TEMPLATES.female.push({id:'char_kaizo_nichijou5_jk_A'"
    c_new = c.replace(s5_first, s4_block + s5_first, 1)
    print(f'Inserted S4 block before S5 first char')

# CHAR_GROUP_DEFS に kaizo_nichijou4 エントリを追加
# kaizo_nichijou5 エントリを探してその前に追加
gd_marker = "{key:'kaizo_nichijou5'"
if gd_marker in c_new:
    gd_entry = "{key:'kaizo_nichijou4',label:'\U0001f3e0\U0001f489\u2620\u72c2\u6c17\u6539\u9020S4',fn:id => /^char_kaizo_nichijou4_/.test(id)},"
    c_new = c_new.replace(gd_marker, gd_entry + "\n" + gd_marker, 1)
    print('Added CHAR_GROUP_DEFS entry')

# CHAR_CATEGORIES に kaizo_nichijou4 エントリを追加
cat_marker = "{ key:'kaizo_nichijou5'"
if cat_marker in c_new:
    cat_entry = "{ key:'kaizo_nichijou4', label:'\U0001f3e0\U0001f489\u2620\u72c2\u6c17\u6539\u9020S4', match: id => /^char_kaizo_nichijou4_/.test(id) },"
    c_new = c_new.replace(cat_marker, cat_entry + "\n  " + cat_marker, 1)
    print('Added CHAR_CATEGORIES entry')

# CHAR_CATEGORY_GROUPS の cats に kaizo_nichijou4 を追加
# kaizo_nichijou5 の前に追加
c_new = re.sub(r"('kaizo_nichijou5')", r"'kaizo_nichijou4', \1", c_new, count=1)
print('Added to CHAR_CATEGORY_GROUPS cats')

# _GP_BIG_GENRE_MAP に追加
genre_label = '\U0001f489 \u6539\u9020\u30fb\u6d17\u8133'
c_new = re.sub(r"('kaizo_nichijou5':'[^']*')", lambda m: f"'kaizo_nichijou4':'{genre_label}', " + m.group(1), c_new, count=1)
print('Added to _GP_BIG_GENRE_MAP')

# バージョン更新
m = re.search(r"name=['\"]version['\"] content=['\"](\d+)['\"]", c_new)
if m:
    old_ver = m.group(1)
    new_ver = str(int(old_ver) + 1)
    c_new = c_new.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f'Version: {old_ver} -> {new_ver}')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(c_new)
print(f'Saved. Added {len(S4_CHARS)} S4 chars.')

# 構文チェック用にJS部分を抽出
import subprocess
result = subprocess.run(['node', '--check', html_path], capture_output=True, text=True)
if result.returncode == 0:
    print('JS syntax: OK')
else:
    print('JS syntax ERROR:', result.stderr[:300])
