"""
覚醒剤 S1/S2/S3 にピーチ姫・甘露寺蜜璃を追加
S1: jk_Aの29シーンをキャラプロンプト置換
S2: S2_tifaの30シーンをキャラプロンプト置換
S3: 新規30シーン
"""
import sys, re, json, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# ========== ユーティリティ ==========
def extract_outfits_array(content, char_id_str):
    """char_id_str の outfits:[ ... ] を抽出してリターン (raw string)"""
    idx = content.find(char_id_str)
    if idx < 0:
        return None, -1, -1
    oi = content.find('outfits:[', idx)
    if oi < 0:
        return None, -1, -1
    start = content.find('[', oi)
    depth = 0
    in_str = False
    sc = None
    i = start
    while i < len(content):
        c = content[i]
        if in_str:
            if c == '\\': i += 2; continue
            if c == sc: in_str = False
        else:
            if c in ('"', "'"): in_str = True; sc = c
            elif c == '[': depth += 1
            elif c == ']':
                depth -= 1
                if depth == 0:
                    return content[start:i+1], start, i+1
        i += 1
    return None, -1, -1

def parse_json_outfits(raw):
    """JSON形式 {"label":"...","value":"..."} を抽出"""
    return re.findall(r'\{"label":\s*"([^"]+)",\s*"value":\s*"([^"]+)"\}', raw)

def parse_js_outfits(raw):
    """JS形式 {'label':'...','value':'...'} を抽出"""
    results = []
    for m in re.finditer(r"\{'label':'((?:[^'\\]|\\.)*)','value':'((?:[^'\\]|\\.)*)'\}", raw):
        results.append((m.group(1), m.group(2)))
    return results

def make_js_outfits(pairs):
    items = []
    for label, value in pairs:
        le = label.replace("'", "\\'")
        ve = value.replace("'", "\\'")
        items.append(f"{{'label':'{le}','value':'{ve}'}}")
    return "[" + ",".join(items) + "]"

def replace_char_prompt(value, old_char, new_char):
    """valueの中のキャラプロンプト部分を置換"""
    return value.replace(old_char, new_char)

# ========== キャラプロンプト定義 ==========
S1_JK_CHAR = "(teenage girl:1.8),(young:1.7),(slender:1.6),(small breasts:1.5),(jk:1.6),16 years old,158cm,black long straight hair,school uniform"

# ピーチ姫 (Princess Peach)
PEACH_CHAR = "(Princess Peach:1.5),(Super Mario:1.35),(blonde hair:1.3),(blue eyes:1.2),(medium breasts:1.4),(slender body:1.3),(pink princess dress:1.2),(golden crown:1.2),(white gloves:1.1)"
PEACH_NEG  = "(adult:1.2),(mature:1.4),(middle aged:1.5),watermark,signature,multiple girls"

# 甘露寺蜜璃 (Kanroji Mitsuri)
MITSURI_CHAR = "(Kanroji Mitsuri:1.5),(Demon Slayer:1.35),(long pink green gradient hair:1.3),(green eyes:1.2),(large breasts:1.6),(voluptuous body:1.4),(love pillar uniform:1.2),(pink haori:1.1),(revealing uniform:1.1)"
MITSURI_NEG  = "(adult:1.2),(mature:1.4),(middle aged:1.5),watermark,signature,multiple girls"

# S2 tifa のキャラプロンプト（置換元）
S2_TIFA_CHAR = "Tifa Lockhart,Final Fantasy VII,long black hair dolphin-tail split,red eyes,athletic"

# S2 aerith のキャラプロンプト（置換元・使わないが念のため）
S2_AERITH_CHAR = "Aerith Gainsborough,Final Fantasy VII,light brown hair ponytail pink ribbon,green eyes"

# ========== S1: jk_Aの29シーンから生成 ==========
print("=== S1 ===")
s1_raw, _, _ = extract_outfits_array(content, "char_kakuseizai_jk_A'")
s1_outfits = parse_json_outfits(s1_raw)
print(f"S1 jk_A outfits: {len(s1_outfits)}")

def make_s1_outfits(outfits, new_char):
    pairs = []
    for label, value in outfits:
        nv = value.replace(S1_JK_CHAR, new_char)
        pairs.append((label, nv))
    return make_js_outfits(pairs)

peach_s1_js   = make_s1_outfits(s1_outfits, PEACH_CHAR)
mitsuri_s1_js = make_s1_outfits(s1_outfits, MITSURI_CHAR)

# ========== S2: S2_tifaの30シーンから生成 ==========
print("=== S2 ===")
s2_raw, _, _ = extract_outfits_array(content, "char_kakuseizai_s2_tifa'")
# S2はJSON形式
s2_outfits = parse_json_outfits(s2_raw)
if not s2_outfits:
    s2_outfits = parse_js_outfits(s2_raw)
    print(f"S2 tifa outfits (JS): {len(s2_outfits)}")
else:
    print(f"S2 tifa outfits (JSON): {len(s2_outfits)}")

# S2のvalue内のS2_TIFA_CHARを置換してピーチ・蜜璃に
def make_s2_outfits(outfits, new_char):
    pairs = []
    for label, value in outfits:
        nv = value.replace(S2_TIFA_CHAR, new_char)
        pairs.append((label, nv))
    return make_js_outfits(pairs)

peach_s2_js   = make_s2_outfits(s2_outfits, PEACH_CHAR)
mitsuri_s2_js = make_s2_outfits(s2_outfits, MITSURI_CHAR)

# ========== S3: 新規30シーン ==========
print("=== S3 ===")
S3_SCENES_PEACH = [
    ("00_強制薬物投与「お城でもこうなる」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,blue eyes,pink princess dress partially disheveled,crown askew,forcefully injected drug into neck vein,syringe in neck,terror expression,wide open eyes,tears starting,dim dungeon,full body"),
    ("01_薬物効果開始「魔法より怖い」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,blue eyes,pink princess dress,crown falling off,drug taking effect,flushed face,confused dazed expression,half lidded eyes,slumped against wall,upper body"),
    ("02_強制服従「姫様も従う」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,blue eyes,pink dress torn at shoulders,crown missing,kneeling submissive pose,obedient vacant smile,slave collar,brand mark,dim room"),
    ("03_複数投与「お城の外では通用しない」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,blue eyes,pink dress disheveled,multiple syringe marks on arm,heavily drugged,dazed vacant eyes,drooling,sitting slumped,upper body"),
    ("04_人形化「姫はもう人形」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,blue eyes,pink dress gone,ownership brand,slave collar,full body tattoos,vacant empty stare,no will,motionless,standing doll pose"),
    ("05_性行為開始「救いは来ない」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,blue eyes,dress completely torn,nipple piercings,vaginal piercings,pained ahegao expression,tears rolling,dim dungeon,full body"),
    ("06_輪姦「姫の肩書きは消えた」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,blue eyes,completely nude,multiple cum marks on body,gang bang aftermath,hollow eyes,tear stained face,lying collapsed"),
    ("07_道具化「コマとして使われる」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,blue eyes,nude,slave collar,ownership mark,brand mark,on all fours like a pet,vacant drugged expression,collar leash attached"),
    ("08_廃人化進行「もう姫ではない」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair tangled,blue eyes glazed,nude,body covered in marks,heavy addiction,hollow empty eyes,lying collapsed,no expression,pale dull skin"),
    ("09_完全廃人「空のお姫様」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair disheveled,dead eyes no highlights,nude,completely vacant face,mouth hanging open,no soul,pale skin,lying on floor,full body"),
    ("10_撮影商品化「記念に残す」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,blue eyes glazed,nude,slave number tattoo,presented for camera,vacant smile,ownership brand,kneeling pose,dim studio light"),
    ("11_自己注射「もう自分でやる」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair unkempt,glazed eyes,nude,self injecting drug into arm,trembling hands,desperate expression,drug addiction,dim room"),
    ("12_三穴同時「全部塞がれた」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair wild,ahegao,nude,all holes used,triple penetration aftermath,body trembling,cum everywhere,collapsed"),
    ("13_意識消失前「最後の意識」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,blue eyes rolling back,nude,drug overdose,convulsing slightly,final moments of consciousness,pale skin,floor"),
    ("14_保存容器「コレクション入り」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,dead eyes,nude,slave collar,ownership brand,numbered tattoo,presented as object,vacant shell,kneeling on display"),
    ("15_心拍危機「消えそうな光」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair sweaty,eyes barely open,nude,extreme drug overdose,cardiac distress,pale sweating skin,barely breathing,lying on side"),
    ("16_神経焼却「もう感じない」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,completely blank eyes,nude,nervous system damage,no reaction,like a doll,lying flat,no expression whatsoever"),
    ("17_苦痛逆転「痛みが快楽になった」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair wild,ahegao pleasure despite pain,nude,pain pleasure inversion,body marked and used,expression of twisted pleasure"),
    ("18_廃棄前最終使用「最後の一度」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair matted,barely conscious,nude,being used one last time,hollow vacant eyes,no resistance,body limp"),
    ("19_魂の残骸「名前も忘れた」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair tangled,dead eyes,nude,complete mental breakdown,no identity remaining,empty expression,sitting against wall,hollow shell"),
    ("20_肉体の限界「体が悲鳴を上げる」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,eyes half open,nude,physical limit reached,body covered in marks,trembling barely upright,exhausted beyond limit"),
    ("21_失禁絶頂「制御を失った」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair wild,ahegao squirt orgasm,nude,involuntary climax,drug forced orgasm,body convulsing,wet floor,no control"),
    ("22_条件反射のみ残る「動物になった」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,blank animal eyes,nude,only reflexes remain,no higher thought,responding only to stimulus,on all fours"),
    ("23_嘔吐と絶頂「体の拒絶と服従」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair messy,simultaneous vomit orgasm expression,nude,body rejecting and climaxing simultaneously,tears,drool"),
    ("24_電子首輪「外れることはない」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,obedient eyes,nude,electronic slave collar activated,shock collar,controlled expression,kneeling obedient"),
    ("25_品評会「展示物になった」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair combed presentably,vacant pretty eyes,nude,on display stage,slave number,ownership brand,presented to buyers"),
    ("26_グループ共有財産「誰のものでもない」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,shared property expression,nude,group ownership marks,multiple brand marks,vacant shared smile,communal property"),
    ("27_意識なく連続使用「眠ったまま」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair spread on floor,unconscious,nude,used while unconscious,cum on body,no awareness,limp sleeping face"),
    ("28_薬液まみれ「内側から溶けていく」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair wet,glazed skin,nude,covered in drug fluid,injection marks everywhere,skin glistening with drugs,hollow"),
    ("29_空の器「何もなくなった」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Princess Peach,Super Mario,blonde hair,completely dead eyes,nude,empty vessel,no soul,no expression,no identity,pale dull skin,lying still,full body"),
]

S3_SCENES_MITSURI = [
    ("00_強制薬物投与「柱もこうなる」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,long pink green hair,green eyes,love pillar uniform disheveled,forcefully injected drug into neck vein,syringe in neck,terror expression,wide open eyes,tears,dim room,full body"),
    ("01_薬物効果開始「炎は消えていく」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair,green eyes,uniform partially undone,drug taking effect,flushed face,confused dazed expression,slumped,upper body"),
    ("02_強制服従「愛の呼吸も使えない」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair,green eyes,uniform torn,kneeling submissive,obedient vacant smile,slave collar,ownership brand,dim room"),
    ("03_複数投与「柱の体が溶ける」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair disheveled,multiple injection marks on arm,heavily drugged,dazed vacant eyes,drooling,slumped sitting,upper body"),
    ("04_人形化「蜜璃はもう蜜璃じゃない」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair,green eyes glazed,uniform gone,slave collar,body tattoos,nipple piercings,vacant empty stare,no will,doll pose"),
    ("05_性行為開始「体が言うことを聞かない」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair wild,nude,large breasts,nipple piercings,vaginal piercings,pained ahegao,tears rolling,full body"),
    ("06_輪姦「柱の名は消えた」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair wild,ahegao,nude,large breasts,cum everywhere,gang bang aftermath,hollow eyes,collapsed"),
    ("07_道具化「愛を感じる体が道具に」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair,nude,large breasts,slave collar,ownership mark,brand mark,on all fours,vacant drugged expression"),
    ("08_廃人化進行「もう鬼殺隊員ではない」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair tangled,nude,large breasts,body marks,hollow empty eyes,lying collapsed,pale dull skin,no expression"),
    ("09_完全廃人「空の柱」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair disheveled,dead eyes,nude,completely vacant face,mouth hanging open,no soul,pale skin,lying on floor"),
    ("10_撮影商品化「証拠として残す」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair,glazed eyes,nude,large breasts,slave number tattoo,presented for camera,vacant smile,kneeling"),
    ("11_自己注射「自分でやるようになった」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair unkempt,glazed eyes,nude,self injecting drug,trembling hands,desperate expression,drug addiction"),
    ("12_三穴同時「全部使われた」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair wild,ahegao,nude,large breasts,triple penetration aftermath,cum everywhere,collapsed trembling"),
    ("13_意識消失前「最後の炎」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair,eyes rolling back,nude,drug overdose,convulsing,final consciousness,pale skin,floor"),
    ("14_保存容器「コレクション入り」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair,dead eyes,nude,slave collar,ownership brand,numbered tattoo,presented as object,kneeling on display"),
    ("15_心拍危機「消えそうな命」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair sweaty,eyes barely open,nude,extreme drug overdose,cardiac distress,pale sweating skin,barely breathing"),
    ("16_神経焼却「愛の呼吸は封じられた」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair,completely blank eyes,nude,nervous system damage,no reaction,like a doll,lying flat"),
    ("17_苦痛逆転「痛みが気持ちよくなった」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair wild,ahegao pleasure despite pain,nude,large breasts,pain pleasure inversion,expression of twisted pleasure"),
    ("18_廃棄前最終使用「最後の一度」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair matted,barely conscious,nude,used one last time,hollow vacant eyes,no resistance,limp"),
    ("19_魂の残骸「蜜璃という名前も消えた」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair tangled,dead eyes,nude,complete mental breakdown,no identity,empty expression,hollow shell"),
    ("20_肉体の限界「体が砕ける」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair,eyes half open,nude,large breasts,physical limit reached,body covered in marks,trembling barely upright"),
    ("21_失禁絶頂「柱でも制御できない」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair wild,ahegao squirt orgasm,nude,large breasts,involuntary climax,drug forced orgasm,body convulsing,wet"),
    ("22_条件反射のみ残る「本能だけが動く」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair,blank animal eyes,nude,only reflexes remain,no higher thought,on all fours,animal instinct only"),
    ("23_嘔吐と絶頂「体の限界超えた」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair messy,simultaneous vomit orgasm,nude,body at absolute limit,tears,drool,vomit,climax simultaneously"),
    ("24_電子首輪「外せない首輪」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair,obedient eyes,nude,electronic slave collar activated,shock collar,controlled expression,kneeling obedient"),
    ("25_品評会「展示される柱」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair combed,vacant pretty eyes,nude,large breasts,on display stage,slave number,ownership brand,presented"),
    ("26_グループ共有財産「誰のものにもなった」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair,shared property expression,nude,group ownership marks,multiple brands,vacant shared smile"),
    ("27_意識なく連続使用「眠ったまま使われる」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair spread,unconscious,nude,large breasts,used while unconscious,cum on body,limp sleeping face"),
    ("28_薬液まみれ「体の中から溶ける」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair wet,glazed skin,nude,covered in drug fluid,injection marks,glistening with drugs,hollow expression"),
    ("29_空の器「愛も消えた」",
     "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(only one girl:1.8),Kanroji Mitsuri,Demon Slayer,pink green hair,completely dead eyes,nude,empty vessel,no soul,no expression,no identity,pale dull skin,lying still"),
]

def scenes_to_js(scenes):
    items = []
    for label, value in scenes:
        le = label.replace("'", "\\'")
        ve = value.replace("'", "\\'")
        items.append(f"{{'label':'{le}','value':'{ve}'}}")
    return "[" + ",".join(items) + "]"

peach_s3_js   = scenes_to_js(S3_SCENES_PEACH)
mitsuri_s3_js = scenes_to_js(S3_SCENES_MITSURI)

# ========== キャラブロック生成 ==========
def char_block(char_id, label, prompt, neg, outfits_js):
    p = prompt.replace("'", "\\'")
    n = neg.replace("'", "\\'")
    return f""",
{{
  id:'{char_id}',label:"{label}",gender:'female',
  prompt:'{p}',
  neg:'{n}',
  outfits:{outfits_js}
}}"""

# S1 (kakuseizai_xxx) の最後に追加 → aerithの後
# S2 (kakuseizai_s2_xxx) の最後に追加 → s2_aerithの後
# S3 (kakuseizai_s3_xxx) の最後に追加 → s3_ff_aerithの後

def find_char_block_end(content, char_id_str):
    """キャラブロックの } の位置を返す"""
    idx = content.find(char_id_str)
    if idx < 0: return -1
    raw, _, end = extract_outfits_array(content, char_id_str)
    if end < 0: return -1
    close = content.find('\n}', end)
    return close + 2

# S1: char_kakuseizai_aerith の後
s1_insert = find_char_block_end(content, "char_kakuseizai_aerith'")
print(f"S1 insert pos: {s1_insert}, context: {content[s1_insert-5:s1_insert+30]!r}")

# S2: char_kakuseizai_s2_aerith の後
s2_insert = find_char_block_end(content, "char_kakuseizai_s2_aerith'")
print(f"S2 insert pos: {s2_insert}, context: {content[s2_insert-5:s2_insert+30]!r}")

# S3: char_kakuseizai_s3_ff_aerith の後
s3_insert = find_char_block_end(content, "char_kakuseizai_s3_ff_aerith'")
print(f"S3 insert pos: {s3_insert}, context: {content[s3_insert-5:s3_insert+30]!r}")

if -1 in (s1_insert, s2_insert, s3_insert):
    print("ERROR: 挿入位置が見つからない")
    sys.exit(1)

# S3を先に挿入（後ろから挿入して位置ずれを防ぐ）
blocks_s3 = (
    char_block('char_kakuseizai_s3_peach',   '💊覚醒剤S3 👸ピーチ姫',   PEACH_CHAR,   PEACH_NEG,   peach_s3_js) +
    char_block('char_kakuseizai_s3_mitsuri', '💊覚醒剤S3 🌸甘露寺蜜璃', MITSURI_CHAR, MITSURI_NEG, mitsuri_s3_js)
)
blocks_s2 = (
    char_block('char_kakuseizai_s2_peach',   '💊覚醒剤S2 👸ピーチ姫',   PEACH_CHAR,   PEACH_NEG,   peach_s2_js) +
    char_block('char_kakuseizai_s2_mitsuri', '💊覚醒剤S2 🌸甘露寺蜜璃', MITSURI_CHAR, MITSURI_NEG, mitsuri_s2_js)
)
blocks_s1 = (
    char_block('char_kakuseizai_peach',   '💊覚醒剤S1 👸ピーチ姫',   PEACH_CHAR,   PEACH_NEG,   peach_s1_js) +
    char_block('char_kakuseizai_mitsuri', '💊覚醒剤S1 🌸甘露寺蜜璃', MITSURI_CHAR, MITSURI_NEG, mitsuri_s1_js)
)

# 後ろから挿入（位置ずれなし）
# 順序: s3_insert > s2_insert > s1_insert の場合が多い
positions = sorted([(s3_insert, blocks_s3), (s2_insert, blocks_s2), (s1_insert, blocks_s1)], reverse=True)
new_content = content
for pos, block in positions:
    new_content = new_content[:pos] + block + new_content[pos:]

# バージョン更新
ver_m = re.search(r'content="(\d{10,})"', new_content)
if ver_m:
    old_ver = ver_m.group(1)
    new_ver = str(int(old_ver) + 1)
    new_content = new_content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f"Version: {old_ver} -> {new_ver}")

backup = r'C:\AI\ComfyUI\dashboard_backup_peach_mitsu_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html'
shutil.copy2(path, backup)
print(f"Backup: {backup}")

with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Saved.")

# 確認
for cid in ['char_kakuseizai_peach', 'char_kakuseizai_mitsuri',
            'char_kakuseizai_s2_peach', 'char_kakuseizai_s2_mitsuri',
            'char_kakuseizai_s3_peach', 'char_kakuseizai_s3_mitsuri']:
    found = f"id:'{cid}'" in new_content
    print(f"  {cid}: {'OK' if found else 'MISSING'}")
