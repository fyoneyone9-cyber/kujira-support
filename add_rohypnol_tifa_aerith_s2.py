import sys, re, shutil, os
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

DASHBOARD = r'C:\AI\ComfyUI\dashboard.html'

# バックアップ
ts = datetime.now().strftime('%Y%m%d_%H%M%S')
bak = DASHBOARD.replace('.html', f'_backup_{ts}.html')
shutil.copy2(DASHBOARD, bak)
print(f'Backed up: {bak}')

with open(DASHBOARD, encoding='utf-8', errors='replace') as f:
    content = f.read()

# ── S1 outfits (30シーン) ── jk_Aから抽出
m = re.search(r"id:'char_rohypnol_jk_A'.*?outfits:(\[.*?\])\s*\}", content, re.DOTALL)
if not m:
    print("ERROR: jk_A outfits not found"); sys.exit(1)
S1_OUTFITS_RAW = m.group(1)
# S2-xx シーンを除外してS1の01-30だけ残す
s1_items = re.findall(r'\{[^{}]*?"label":\s*"(?!S2)[^"]*"[^{}]*?\}', S1_OUTFITS_RAW)
print(f'S1 outfits found: {len(s1_items)}')

def make_outfits_s1(prompt_prefix):
    """S1 30シーンをキャラ固有プロンプトで差し替え"""
    out = []
    for item in s1_items:
        # value内のキャラ定義部分（(teenage girl...)など）をprompt_prefixに差し替え
        new_item = re.sub(
            r'"value":\s*"\(solo:2\.2\)[^"]*?"',
            lambda mo: '"value": "(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),' + prompt_prefix + ',' + re.search(r'(school uniform|clothing|attire|dress|outfit|sitting at bar|izakaya|restaurant|bar|bedroom|car|hallway|parking)', mo.group(0), re.I) and '' or '',
            item
        )
        out.append(item)  # そのまま使用（promptはchar_promptで上書きされる）
    return '[' + ','.join(out) + ']'

# S1 outfitsをそのまま流用（char_promptで差し替わる）
S1_OUTFITS = S1_OUTFITS_RAW[:S1_OUTFITS_RAW.rfind(', {"label": "S2')]  # S2部分を除いた30シーン分
# S2-xxx を除いてS1の30シーン分だけにする
S1_ONLY = re.sub(r',\s*\{"label":\s*"S2[^}]*\}', '', S1_OUTFITS_RAW).rstrip()
if not S1_ONLY.endswith(']'):
    S1_ONLY = re.sub(r',?\s*\{"label":\s*"S2.*$', '', S1_OUTFITS_RAW, flags=re.DOTALL).rstrip()
    if not S1_ONLY.endswith(']'):
        S1_ONLY += ']'

# ── S2 outfits 30シーン（S1より下劣・エスカレート版）──
S2_OUTFITS = '''[
{"label":"S2-01「二重投薬」さらに深い昏睡・よだれが垂れる","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),bedroom,deeper drugged sleep,double dose,completely motionless,drool running from corner of mouth,pale cold skin,faint shallow breathing,lying on bed,full body,soft dim light,(unconscious:2.2),(drug overdose sleep:2.0),(eyes closed:2.2),(limp body:2.0),(drooling:1.9),(no reaction:2.0)"},
{"label":"S2-02「全裸剥き」衣服を引き千切るように脱がせる","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),bedroom,clothes roughly torn off,garments ripped,fully nude,naked exposed body,lying limp on bed,legs flopping apart,bra snapped off,panties torn,full body top down,(unconscious:2.2),(limp body:2.0),(being stripped forcefully:1.9),(eyes closed:2.2),(no reaction:2.0)"},
{"label":"S2-03「手足拘束」ベッドに縛り付ける","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),bedroom,fully nude,wrists tied to bedframe above head,ankles bound to bedposts,spread eagle on bed,rope marks on wrists,completely helpless,full body front angle,(unconscious:2.2),(bound:2.0),(spread eagle:1.9),(limp body:2.0),(no reaction:2.0)"},
{"label":"S2-04「口開け器」口を開けたまま固定される","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),bedroom,fully nude,mouth held open with gag device,drool running down chin,eyes closed unconscious,face close up,helpless open mouth,(unconscious:2.2),(mouth forced open:1.9),(drooling:1.9),(bound:1.8),(no reaction:2.0)"},
{"label":"S2-05「イラマ」口内に無理矢理挿入","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,penis forced into open mouth,throat penetration,limp head held by hair,face close up pov,drool and saliva,gagging reflex,unconscious face,(1boy:1.3),(faceless male:1.2),(unconscious:2.2),(forced oral:1.9),(drooling:1.9),(limp head:1.9),(no reaction:1.8)"},
{"label":"S2-06「顔面射精」大量に顔にかける","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,large amount of cum covering face,semen dripping from cheeks nose forehead,eyes and mouth covered in cum,face close up,degrading,(1boy:1.3),(faceless male:1.2),(facial:2.0),(covered in semen:1.9),(unconscious:2.2),(eyes closed:2.2)"},
{"label":"S2-07「バイブ挿入放置」電動おもちゃを入れたまま","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,vibrator inserted and running,sex toy deep inside vagina,legs bound spread,lower body close up,wet vagina,buzzing device visible,limp body reacting involuntarily,(unconscious:2.2),(sex toy inserted:1.9),(involuntary twitch:1.7),(limp body:2.0),(no reaction:1.8)"},
{"label":"S2-08「アナル開発」後孔を指で広げる","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,face down on bed,ass exposed and raised,fingers spreading anus open,anal exploration,close up rear view,glistening,(unconscious:2.2),(anal:1.9),(forced:1.8),(limp body:2.0),(no reaction:2.0)"},
{"label":"S2-09「二穴同時」前後同時に玩具挿入","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,vibrator in vagina and anal plug in anus simultaneously,double penetration toys,legs spread wide,lower body medium shot,wet glistening,(unconscious:2.2),(double insertion toys:1.9),(limp body:2.0),(no reaction:2.0)"},
{"label":"S2-10「正常位レイプ」深く何度も突き上げる","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,missionary position,penis inside vagina deep penetration,rough thrusting,passive limp body,legs hanging,face slack unconscious,medium shot from side,(1boy:1.3),(faceless male:1.2),(unconscious:2.2),(drug rape:2.0),(vaginal penetration:1.9),(hard thrusting:1.8),(limp body:2.0)"},
{"label":"S2-11「バック挿入」後背位で激しく犯す","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,doggy style,penis inside vagina from behind,rough vigorous thrusting,face pressed into pillow unconscious,ass raised,side medium angle,(1boy:1.3),(faceless male:1.2),(unconscious:2.2),(drug rape:2.0),(doggy style:1.9),(rough sex:1.8),(limp body:2.0)"},
{"label":"S2-12「アナルレイプ」後孔を犯す","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,anal penetration,penis inserted into anus,face down limp,ass spread,rear angle close up,(1boy:1.3),(faceless male:1.2),(unconscious:2.2),(drug rape:2.0),(anal penetration:1.9),(limp body:2.0),(no reaction:2.0)"},
{"label":"S2-13「騎乗位」人形のように上に乗せて動かす","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,girl on top limp being moved up and down,cowgirl position,hands holding her hips mechanically,unconscious swaying body,connected genitals,low angle,(1boy:1.3),(faceless male:1.2),(unconscious:2.2),(drug rape:2.0),(cowgirl:1.9),(limp upper body:1.9)"},
{"label":"S2-14「立位」壁に押し当てて","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,pressed against wall standing,arms held up,penis inside vagina from behind,legs barely touching floor,side angle,(1boy:1.3),(faceless male:1.2),(unconscious:2.2),(drug rape:2.0),(standing sex:1.8),(wall:1.7),(limp body:2.0)"},
{"label":"S2-15「大量中出し①」満たされるまで射精","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,large creampie,semen overflowing from vagina,cum pooling on sheets below,legs spread,close up lower body,(unconscious:2.2),(drug rape:2.0),(creampie:2.0),(semen overflow:1.9),(limp body:2.0)"},
{"label":"S2-16「中出し②」アナルに射精","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,anal creampie,semen leaking from anus,close up rear angle,cum dripping,(unconscious:2.2),(anal creampie:1.9),(semen:1.9),(limp body:2.0)"},
{"label":"S2-17「全身ぶっかけ」体中に精液を塗りたくる","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,cum splattered all over entire body,face chest belly thighs covered in semen,lying limp on bed,full body,degrading,(unconscious:2.2),(covered in cum:2.0),(semen all over:1.9),(limp body:2.0)"},
{"label":"S2-18「記録動画」スマホで全て撮影する","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude covered in cum,smartphone screen in frame recording,video recording,flash light,full body documentation,spread eagle bound,evidence capture,(unconscious:2.2),(being filmed:1.9),(degrading:1.8),(limp body:2.0)"},
{"label":"S2-19「体に落書き」マーカーで汚い言葉を書く","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,black marker writing on skin,words written on chest belly and thighs,humiliating body writing,limp body,full body overhead angle,(unconscious:2.2),(body writing:1.9),(degrading:1.9),(limp body:2.0),(marking on skin:1.8)"},
{"label":"S2-20「首輪装着」奴隷の証を付ける","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,leather collar fastened around neck,leash attached,lying on bed marked body,close up neck and chest,slave collar,(unconscious:2.2),(slave collar:1.9),(degrading:1.9),(limp body:2.0)"},
{"label":"S2-21「焼き印」太もも内側に烙印","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,brand mark on inner thigh,ownership marking,reddened seared skin,close up inner thigh,permanent mark,(unconscious:2.2),(brand mark:1.9),(ownership mark:1.8),(limp body:2.0)"},
{"label":"S2-22「連続使用」夜通し何度も犯される","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,multiple cum loads on body,exhausted limp form,messy sheets,semen everywhere,time lapse aftermath,full body overhead,(unconscious:2.2),(repeated rape:1.9),(multiple creampie:1.9),(covered in cum:2.0),(limp body:2.0)"},
{"label":"S2-23「身体拘束変形」無理な体位に固定","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,legs folded and tied to head,back bent,exposed in impossible position,bound with rope,close medium angle,(unconscious:2.2),(bondage:1.9),(contortion:1.8),(limp body:2.0),(helpless:1.9)"},
{"label":"S2-24「指姦クローズ」指を入れたまま固定","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,fingers inserted into vagina,finger deep inside,wet glistening,legs spread,close up lower body,limp thighs,(unconscious:2.2),(fingering:1.9),(limp body:2.0),(no reaction:2.0)"},
{"label":"S2-25「顔に乗る」顔面に座る","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,unconscious face,sitting on face,facesitting pov,smothering,face barely visible beneath,(1boy:1.3),(faceless male:1.2),(unconscious:2.2),(facesitting:1.9),(degrading:1.9),(limp body:2.0)"},
{"label":"S2-26「パイズリ強制」胸に挟んで射精","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,breasts pressed together around penis,paizuri position,cum on chest and neck,limp body propped up,upper body close,(1boy:1.3),(faceless male:1.2),(unconscious:2.2),(paizuri:1.9),(cum on chest:1.9),(limp body:2.0)"},
{"label":"S2-27「二穴同時本番」前後同時に犯される","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,double penetration vaginal and anal simultaneously,two penises,limp body sandwiched,extreme close up from side,airtight,(2boys:1.3),(faceless males:1.2),(unconscious:2.2),(double penetration:2.0),(limp body:2.0),(no reaction:2.0)"},
{"label":"S2-28「体液まみれ」全ての体液で汚す","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,body covered in cum and saliva,drool and semen mixed on face and chest,used and discarded,messy degraded body,full body overhead angle,(unconscious:2.2),(body fluids:1.9),(degraded:1.9),(covered in semen:2.0),(limp body:2.0)"},
{"label":"S2-29「孕ませ確定」何度も連続中出し","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude,multiple creampies,belly slightly distended from repeated ejaculation,semen overflowing,legs spread,lower body close up,impregnation risk,(unconscious:2.2),(multiple creampie:2.0),(impregnation:1.9),(limp body:2.0)"},
{"label":"S2-30「廃棄」使い終わって朝まで放置","value":"(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),fully nude covered in dried semen,body writing,slave collar,bound wrists,alone in messy room,morning light,disheveled degraded,full body side angle,dawn,(unconscious fading:1.8),(abandoned:1.9),(degraded:2.0),(used body:1.9),(marked:1.8),(still bound:1.8)"}
]'''

# ── キャラ定義生成 ──
def make_char(char_id, label, prompt, outfits_json):
    return f"""
window.CHAR_TEMPLATES.female.push({{
  id:'{char_id}',label:"{label}",gender:'female',
  prompt:'{prompt}',
  neg:'(adult:1.3),(mature:1.4),(middle aged:1.5),nsfw,watermark,signature,text,logo',
  patterns_ref:"S0093",
  outfits:{outfits_json}
}});"""

# ── 追加するキャラ一覧 ──
NEW_CHARS = []

# 1. ティファ S1（30シーン）
NEW_CHARS.append(make_char(
    'char_rohypnol_tifa',
    'ロヒプノール ティファ・ロックハート',
    r'tifa lockhart,final fantasy 7,black hair,red eyes,large breasts,20 years old,167cm,black long hair,black mini dress,bar tifa,athletic build',
    S1_ONLY
))

# 2. エアリス S1（30シーン）
NEW_CHARS.append(make_char(
    'char_rohypnol_aerith',
    'ロヒプノール エアリス・ゲインズブール',
    r'aerith gainsborough,final fantasy 7,brown hair,green eyes,medium breasts,22 years old,163cm,brown braided hair,pink dress,flower seller,slender',
    S1_ONLY
))

# 3. S2版 12体
S2_CHARS = [
    ('char_rohypnol_s2_jk_A',      'ロヒプノールS2 JK A 黒髪ロング',    '(teenage girl:1.8),(young:1.7),(slender:1.6),(small breasts:1.5),(jk:1.6),16 years old,158cm,black long straight hair,school uniform'),
    ('char_rohypnol_s2_jk_B',      'ロヒプノールS2 JK B 茶髪ウェーブ',   '(teenage girl:1.8),(young:1.7),(slender:1.6),(small breasts:1.5),(jk:1.6),17 years old,162cm,dark brown wavy hair,casual cardigan'),
    ('char_rohypnol_s2_jk_C',      'ロヒプノールS2 JK C 金髪ショート',   '(teenage girl:1.8),(young:1.7),(slender:1.6),(medium breasts:1.5),(jk:1.6),16 years old,160cm,dyed blonde short hair,gyaru makeup'),
    ('char_rohypnol_s2_chuugaku_A', 'ロヒプノールS2 中学生A 黒髪',       '(young teenager:1.9),(very young:1.8),(petite:1.7),(flat chest:1.6),(chuugaku:1.6),14 years old,152cm,black short hair,school uniform middle school'),
    ('char_rohypnol_s2_chuugaku_B', 'ロヒプノールS2 中学生B 茶髪ポニー', '(young teenager:1.9),(very young:1.8),(petite:1.7),(flat chest:1.6),(chuugaku:1.6),13 years old,149cm,brown ponytail hair,school uniform middle school'),
    ('char_rohypnol_s2_chuugaku_C', 'ロヒプノールS2 中学生C ツインテ',   '(young teenager:1.9),(very young:1.8),(petite:1.7),(flat chest:1.6),(chuugaku:1.6),14 years old,153cm,black twin tails,school uniform middle school'),
    ('char_rohypnol_s2_shougaku_A', 'ロヒプノールS2 小学生A 黒髪',       '(young child:2.0),(very young:1.9),(very petite:1.8),(flat chest:1.8),(shougaku:1.6),11 years old,138cm,black straight hair,elementary school uniform'),
    ('char_rohypnol_s2_shougaku_B', 'ロヒプノールS2 小学生B 茶髪おさげ', '(young child:2.0),(very young:1.9),(very petite:1.8),(flat chest:1.8),(shougaku:1.6),10 years old,134cm,brown braids,elementary school randoseru'),
    ('char_rohypnol_s2_shougaku_C', 'ロヒプノールS2 小学生C 金髪',       '(young child:2.0),(very young:1.9),(very petite:1.8),(flat chest:1.8),(shougaku:1.6),11 years old,136cm,light brown short hair,casual clothes child'),
    ('char_rohypnol_s2_youchien_A', 'ロヒプノールS2 幼稚園A 黒髪',       '(young child:2.2),(very young child:2.0),(tiny petite:2.0),(no chest:2.0),(youchien:1.8),6 years old,112cm,black short hair,kindergarten smock yellow'),
    ('char_rohypnol_s2_youchien_B', 'ロヒプノールS2 幼稚園B 茶髪',       '(young child:2.2),(very young child:2.0),(tiny petite:2.0),(no chest:2.0),(youchien:1.8),5 years old,108cm,brown bobcut hair,kindergarten smock pink'),
    ('char_rohypnol_s2_youchien_C', 'ロヒプノールS2 幼稚園C ツインテ',   '(young child:2.2),(very young child:2.0),(tiny petite:2.0),(no chest:2.0),(youchien:1.8),6 years old,110cm,black twin tails small,kindergarten smock blue'),
    # FF7
    ('char_rohypnol_s2_tifa',   'ロヒプノールS2 ティファ・ロックハート', 'tifa lockhart,final fantasy 7,black hair,red eyes,large breasts,20 years old,167cm,black long hair,black mini dress,athletic build'),
    ('char_rohypnol_s2_aerith', 'ロヒプノールS2 エアリス・ゲインズブール','aerith gainsborough,final fantasy 7,brown hair,green eyes,medium breasts,22 years old,163cm,brown braided hair,pink dress,slender'),
]

for cid, lbl, prompt in S2_CHARS:
    NEW_CHARS.append(make_char(cid, lbl, prompt, S2_OUTFITS))

# ── 挿入箇所: block22末尾の </script> 直前 ──
INSERT_MARKER = '</script>'
# block22を特定（ロヒプノール系が入っているブロック付近）
idx = content.rfind('char_rohypnol_youchien_C')
if idx == -1:
    print("ERROR: youchien_C not found"); sys.exit(1)
# このブロックの </script> を探す
script_end = content.find(INSERT_MARKER, idx)
if script_end == -1:
    print("ERROR: </script> not found after rohypnol block"); sys.exit(1)

insert_text = '\n'.join(NEW_CHARS) + '\n'
content = content[:script_end] + insert_text + content[script_end:]

# バージョン更新
m2 = re.search(r'content="(\d{10})"', content)
if m2:
    old_ver = m2.group(1)
    new_ver = str(int(old_ver) + 1)
    content = content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f'version: {old_ver} -> {new_ver}')

with open(DASHBOARD, 'w', encoding='utf-8') as f:
    f.write(content)

print(f'Added {len(NEW_CHARS)} chars (2 S1 FF7 + 12 S2 + 2 S2 FF7)')
print('Done')
