"""
RAPE_COMP_V2 実行タイミング修正
問題: RAPE_COMP_V2はL8835で実行されるが、その時点でwf['6']には初期WFの
      最小テキスト(1girl, japanese程度)しか入っていない。
      full_positiveがwf['6']に書かれるのはL38812。

修正: RAPE_COMP_V2のロジックを full_positive書き込み後に移植する。
      既存のL8885~L9158のif不発火ブロックはコメントアウトする。

なお通常構図(REDCRAFT_COMPOSITION_V3の非rapeブロック)はL8885以降で
_rc3_posをL8842で読むが、こちらも同じ問題があるはず。
ただしRAPE_COMP_V2優先で今回は修正。
"""
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# --- STEP 1: L38812直後の挿入点を探す ---
# "if "6" in wf: wf["6"]["inputs"]["text"]=full_positive"
# の直後に RAPE_COMP_V2 コードを追加する

ANCHOR = 'if "6" in wf: wf["6"]["inputs"]["text"]=full_positive'

# このanchorが複数ある可能性があるので最初の1件（L38812相当）
idx = content.find(ANCHOR)
if idx == -1:
    print('ERROR: anchor not found:', ANCHOR[:60])
    sys.exit(1)

# anchorの行末(改行)の後に挿入
insert_after = content.index('\n', idx) + 1
print(f'挿入位置: char {insert_after}')

RAPE_COMP_CODE = '''
        # [RAPE_COMP_V2_RELOCATED 2026-10-21] ─────────────────────────────────
        # RAPE_COMP_V2を full_positive書き込み後に移動。
        # 理由: 以前はL8835で実行していたが、その時点でwf['6']には初期WFテキスト
        #       (1girl, japanese程度)しか入っておらず、_rc3_is_rapeが常にFalseで
        #       全く発火しなかった。full_positive(outfit含む完成プロンプト)を
        #       見た後に判定するのが正しい。
        try:
            if _is_redcraft_ks and '6' in wf:
                _rc2_pos = wf['6']['inputs'].get('text', '')
                _rc2_lo = _rc2_pos.lower()

                # 性行為シーン・既にアングル指定があればスキップ
                _rc2_skip = any(k in _rc2_lo for k in [
                    'penetration', 'vaginal', 'insertion', 'creampie', 'cowgirl', 'doggy',
                    'missionary', 'prone bone', 'reverse cowgirl', 'blowjob', 'fellatio',
                    'handjob', 'paizuri', 'from behind sex', 'sex pov', 'pov sex',
                    'spy cam', 'hidden cam', 'bondage', 'tied up', 'shibari',
                ])
                _rc2_has_angle = any(k in _rc2_lo for k in [
                    'from above', 'from below', 'from behind', 'from side',
                    'dutch angle', 'low angle', 'high angle', 'worm eye',
                    'three quarter', 'over shoulder', '45 degree', 'slight side',
                    'front view', "bird's eye", 'dynamic angle',
                ])

                _rc2_is_rape = any(k in _rc2_lo for k in [
                    'rape','forced sex','non-consensual','sexual assault',
                    'grabbed','pinned down','held down','dragged','overpowered',
                    'struggling','cannot escape','tied down','wrists held',
                    'being restrained','resistance','abducted','kidnap',
                    'clothes torn','shirt torn','skirt lifted','panties pulled',
                    'being stripped','forced undress','clothes ripped',
                    'after assault','lying limp','collapsed on floor',
                    'body trembling','curled up crying','shaking in corner',
                    'レイプ','強姦','強制','強引','力ずく','無理やり','犯される',
                    '引きずり','押し倒','押さえつ','逃げられない','抵抗','拉致',
                    '監禁','拘束','縛られ','手首を掴','腕を掴','首を掴',
                    '羽交い締め','組み伏','組み敷','乱暴','蹂躙','犯す',
                    '引き込まれ','連れ込まれ','脱がされ','剥ぎ取','服を破',
                    'されるがまま','動けない','身動き','震えながら','泣き崩',
                    '泣きじゃくり','体を震わせ','床に倒れ','うずくまり',
                    # ラベル系（outfit valueに含まれないケース対応）
                    '脱走試み','監禁強化','更なる監禁',
                    '転売','vipクライアント','公開陵辱','永続配信','繁殖プログラム',
                    '催眠','洗脳強化',
                    # 盗撮系
                    '盗撮','upskirt','スカートの中',
                ])

                if _rc2_is_rape and not _rc2_skip and not _rc2_has_angle:
                    import random as _rc2_rand

                    def _rc2_kw(*kws): return any(k in _rc2_lo for k in kws)

                    _rc2_phase = None
                    if _rc2_kw('引きずり','引き込','連れ込','拉致','連行','押し込','押し倒','投げ込','引っ張','部屋に','監禁部屋','dragged','grabbed','abducted','kidnap','forced into','pulled into','pushed into','being pushed','thrown into','shoved into','locked in','chain collar','首にチェーン','collar clicking','chain clicked','collar being locked','チェーンを付','脱走試み','監禁強化','更なる監禁'): _rc2_phase = 'drag'
                    elif _rc2_kw('拘束','縛られ','手足','手首','ロープ','足首','四肢','tied','bound','restrained','rope','cuffed','chained','wrists tied','ankles bound','spread eagle','arms above','arms raised','bound to','fixed in place','cannot move','immobilized','helpless position'): _rc2_phase = 'bound'
                    elif _rc2_kw('脱がされ','剥ぎ取','服を破','服を引き','スカートをめくられ','clothes torn','torn shirt','skirt lifted','panties pulled','being stripped','forced undress','clothes ripped','shirt torn','bra removed','clothes being removed','undressing her','exposed skin','nakedness revealed'): _rc2_phase = 'strip'
                    elif _rc2_kw('妊娠','お腹','臨月','陣痛','出産','胎動','母乳','授乳','産後','破水','いきむ','赤ちゃん','newborn','pregnant','pregnancy','belly','baby','labor pain','contractions','giving birth','postpartum','breast milk','breastfeeding','belly bump','round belly','pregnant belly'): _rc2_phase = 'pregnant'
                    elif _rc2_kw('事後','終わった後','放置','after assault','lying limp','collapsed','curled up','泣き崩','うずくまり','震えながら','体を震','床に倒れ','one arm covering chest','knees drawn up','left alone','abandoned after','sobbing alone','broken','lying on floor','lying face down'): _rc2_phase = 'after'
                    elif _rc2_kw('帰り道','夜道','追跡','後をつけ','足音','一人に','気配','振り返','誰もいない','暗い道','街灯','孤独','footsteps','walking faster','turning to check','alone at night','pursued','being followed','feeling watched','growing uncertain','dark alley','empty street','no one around','shadowed','night road'): _rc2_phase = 'fear'
                    elif _rc2_kw('膝の上','お風呂','ないしょ','パパだけのもの','特別な遊び','大好き','ふたりのひみつ','なついている','パパが好き','lap sitting','bathing together','special secret','bedtime','trusted adult','our secret','just the two','gentle touch','grooming'): _rc2_phase = 'groom'
                    elif _rc2_kw('撮影','記録','カメラ','証拠','写真','カメラを向け','filming','recorded','camera','photograph','on camera','being filmed','posed for','documentation','video','taking photos','snapshot','evidence photo','盗-','盗撮','upskirt','スカートの中','着替え','開脚','前かがみ','突っ伏し','自撮り','体育授業','体操','ジャングルジム','逆立ち','転売','vipクライアント','vip','公開陵辱','永続配信','次世代連鎖','繁殖プログラム','複数組織'): _rc2_phase = 'filming'
                    elif _rc2_kw('感度開発','調教','バイブ','週末は','ルーティン','体が慣れ','conditioning','trained','sensitivity','vibrator','brainwash','mind control','weekly routine','conditioned response','behavioral conditioning','trained to','obedient','submissive posture','催眠','洗脳強化','薬物完全依存','薬物依存','依存させ'): _rc2_phase = 'conditioning'
                    elif _rc2_kw('廃人','感情がなくなった','天井だけ見ていた','もう何も考えない','解離','麻痺','空虚','虚ろ','呆然','完全に疲弊','床で呆然','vacant open eyes','arms limp','head turned sideways','dissociation','blank stare','empty eyes','staring at ceiling','no emotion','mentally absent','thousand yard stare','vacant expression','hollow','numb','detached','lying face down on floor','utterly exhausted'): _rc2_phase = 'dissoc'
                    elif _rc2_kw('pov','first person','looking up at','upward gaze','見上げ','上から','加害者視点','俯瞰','監視','predator pov','from above perspective','looking down at her','voyeur','watching from','observed','close-up face','forced penetr','begging through','please stop','prolonged assault','forcing physical','最初の貫通','懇願する','強制絶頂','屈辱','貫通'): _rc2_phase = 'pov'
                    elif _rc2_kw('触れ','体を触','手が触','なでる','撫で','肌に触','touching','groping','hand on','caressing','feeling up','first touch','body contact','unwanted touch'): _rc2_phase = 'touch'
                    else: _rc2_phase = 'generic'

                    _RC2_POOLS = {
                        'drag': [
                            '(low angle shot:1.5),(from slightly below:1.4),(dynamic tension:1.4),(panic framing:1.4)',
                            '(dutch angle:1.5),(tilted frame:1.5),(disorientation framing:1.4),(urgency:1.3)',
                            '(high angle shot:1.4),(from above:1.4),(full body:1.4),(helplessness framing:1.3)',
                            '(worm eye view:1.5),(extreme low angle:1.5),(looking up at captor:1.4)',
                            '(over shoulder angle:1.4),(corridor perspective:1.3),(forced movement:1.3)',
                            '(close-up:1.4),(face close up:1.4),(terror in eyes:1.4),(door slamming framing:1.3)',
                            '(medium shot:1.4),(chain collar visible:1.3),(dim room:1.3),(concrete floor:1.3)',
                        ],
                        'bound': [
                            '(front view:1.4),(symmetrical framing:1.4),(full body visible:1.4),(spread eagle emphasis:1.3)',
                            '(high angle shot:1.5),(from above:1.5),(looking down at bound figure:1.4)',
                            '(low angle shot:1.4),(from below:1.4),(bound wrists above head:1.4)',
                            '(close-up:1.5),(face close up:1.5),(tear streaked and afraid:1.4)',
                            '(medium shot:1.4),(waist up:1.4),(bound arms visible:1.4),(rope detail:1.3)',
                            '(three quarter view:1.4),(body tension visible:1.3),(restrained posture:1.3)',
                            '(eye level shot:1.4),(direct confrontation angle:1.3),(captive framing:1.3)',
                        ],
                        'strip': [
                            '(medium shot:1.4),(upper body focus:1.4),(clothes being torn:1.3),(shame framing:1.3)',
                            '(high angle shot:1.4),(from above:1.4),(looking down in disgrace:1.4)',
                            '(three quarter view:1.4),(disheveled clothes:1.3),(exposed skin visible:1.3)',
                            '(close-up:1.4),(bust shot:1.4),(torn fabric edge:1.3),(exposed framing:1.3)',
                            '(full body shot:1.4),(clothes in disarray:1.3),(hugging self:1.3)',
                            '(side profile:1.4),(arms covering chest:1.3),(shame posture:1.3)',
                            '(low angle shot:1.4),(from below:1.3),(skirt being lifted:1.3)',
                        ],
                        'pregnant': [
                            '(high angle shot:1.5),(from above:1.4),(large belly visible:1.5),(vulnerability:1.3)',
                            '(eye level shot:1.4),(side profile:1.5),(belly silhouette:1.5),(pregnancy framing:1.4)',
                            '(medium shot:1.4),(waist up:1.4),(hands on belly:1.4),(scared eyes:1.3)',
                            '(close-up:1.5),(belly close up:1.5),(hands pressing on belly:1.4)',
                            '(full body shot:1.4),(full body visible:1.4),(heavily pregnant posture:1.4)',
                            '(low angle shot:1.4),(from below:1.3),(enormous belly from below:1.4)',
                            '(three quarter view:1.4),(profile angle:1.4),(belly profile emphasized:1.4)',
                            '(floor level shot:1.4),(lying on back:1.4),(belly rising:1.3),(exhausted:1.3)',
                        ],
                        'after': [
                            '(high angle shot:1.5),(from above:1.5),(collapsed body below:1.4),(isolation:1.4)',
                            '(floor level shot:1.5),(extreme low angle:1.4),(curled up figure:1.4),(fetal position:1.3)',
                            '(side profile:1.4),(body curled inward:1.4),(grief posture:1.3)',
                            '(three quarter view:1.3),(small figure in large empty room:1.4),(loneliness:1.3)',
                            '(medium shot:1.4),(waist up:1.4),(arms wrapped around self:1.4),(trembling:1.3)',
                            '(close-up:1.5),(face close up:1.5),(tear streaked cheeks:1.4),(despair:1.4)',
                            '(overhead shot:1.5),(directly from above:1.5),(lying on floor:1.4),(broken framing:1.3)',
                        ],
                        'fear': [
                            '(over shoulder angle:1.5),(looking back framing:1.5),(pursued feeling:1.4)',
                            '(high angle shot:1.4),(from above:1.4),(small figure in dark:1.5),(vulnerable:1.3)',
                            '(dutch angle:1.4),(tilted frame:1.4),(psychological unease:1.4)',
                            '(three quarter view:1.4),(turned away:1.4),(looking back over shoulder:1.4)',
                            '(medium shot:1.4),(waist up:1.4),(darkness surrounding:1.4),(alone:1.3)',
                            '(low angle shot:1.4),(from below:1.3),(looming environment:1.3)',
                            '(worm eye view:1.3),(street level:1.3),(empty dark road:1.3)',
                        ],
                        'groom': [
                            '(slight high angle:1.4),(warm soft lighting:1.3),(intimate close framing:1.4),(power dynamic:1.3)',
                            '(medium shot:1.4),(waist up:1.4),(false warmth:1.3),(deceptive safety:1.3)',
                            '(close-up:1.4),(face focus:1.4),(confusion on face:1.3),(mixed emotion:1.3)',
                            '(over shoulder angle:1.3),(adult perspective:1.4),(child small in frame:1.4)',
                            '(three quarter view:1.4),(intimate distance:1.3),(claustrophobic warmth:1.3)',
                            '(eye level shot:1.4),(gentle but wrong framing:1.3),(coercive intimacy:1.3)',
                        ],
                        'filming': [
                            '(front view:1.4),(straight on:1.5),(camera facing:1.4),(documented pose:1.3)',
                            '(full body shot:1.4),(full body visible:1.4),(forced to pose:1.4),(on display:1.3)',
                            '(medium shot:1.4),(upper body:1.4),(camera awareness:1.3),(recorded moment:1.3)',
                            '(slight high angle:1.4),(surveillance angle:1.4),(watched and recorded:1.4)',
                            '(close-up:1.4),(face close up:1.4),(shame on camera:1.4),(tears on film:1.3)',
                            '(three quarter view:1.3),(body displayed:1.4),(exhibit framing:1.3)',
                            '(low angle shot:1.4),(looking up at camera:1.4),(forced compliance:1.3)',
                        ],
                        'conditioning': [
                            '(high angle shot:1.4),(from above:1.5),(submissive figure below:1.4),(dominance:1.3)',
                            '(close-up:1.4),(body reaction focus:1.4),(physiological response:1.3)',
                            '(medium shot:1.4),(waist up:1.4),(passive compliance:1.3),(trained posture:1.3)',
                            '(three quarter view:1.4),(resignation body language:1.3),(conditioned:1.3)',
                            '(side profile:1.4),(limp compliance:1.3),(broken will:1.3)',
                            '(full body shot:1.4),(kneeling position:1.3),(submissive framing:1.3)',
                            '(eye level shot:1.4),(vacant obedience:1.3),(hollow eyes:1.3)',
                        ],
                        'dissoc': [
                            '(close-up:1.5),(face close up:1.5),(vacant eyes:1.5),(empty stare:1.5)',
                            '(overhead shot:1.5),(directly from above:1.4),(small broken figure:1.4)',
                            '(three quarter view:1.3),(distant thousand yard stare:1.4),(absent:1.4)',
                            '(medium shot:1.4),(upper body:1.4),(hollow expression:1.5),(absent presence:1.4)',
                            '(eye level shot:1.4),(direct empty gaze:1.5),(dead inside framing:1.4)',
                            '(side profile:1.4),(looking at nothing:1.5),(mentally gone:1.4)',
                            '(floor level shot:1.4),(lying face down:1.4),(arms limp:1.3),(given up:1.3)',
                        ],
                        'pov': [
                            '(pov:1.5),(first person view:1.5),(looking down at her:1.4),(predator perspective:1.4)',
                            '(high angle shot:1.5),(from above:1.5),(pov dominant:1.4),(looking up at viewer:1.4)',
                            '(extreme close-up:1.4),(pov face close:1.4),(looking up terrified:1.4)',
                            '(worm eye view:1.4),(from floor:1.4),(pov of captor:1.4)',
                            '(medium pov shot:1.4),(waist height pov:1.4),(trapped in frame:1.3)',
                            '(surveillance angle:1.4),(watched from above:1.4),(camera trap framing:1.3)',
                        ],
                        'touch': [
                            '(medium shot:1.4),(waist up:1.4),(unwanted contact framing:1.3),(discomfort:1.3)',
                            '(close-up:1.4),(face reaction:1.4),(disgust and fear:1.4),(flinching:1.3)',
                            '(slight high angle:1.4),(looking down:1.4),(power imbalance touch:1.3)',
                            '(three quarter view:1.4),(body recoiling:1.3),(withdrawal framing:1.3)',
                            '(over shoulder angle:1.4),(intruding hands framing:1.3),(personal space violated:1.3)',
                            '(eye level shot:1.4),(pleading eyes:1.4),(stop framing:1.3)',
                        ],
                        'generic': [
                            '(high angle shot:1.5),(from above:1.4),(power imbalance:1.3)',
                            '(low angle shot:1.4),(from below:1.4),(looking up:1.4)',
                            '(close-up:1.4),(face close up:1.4),(emotional intensity:1.3)',
                            '(three quarter view:1.4),(tension in posture:1.3)',
                            '(dutch angle:1.4),(tilted frame:1.4),(psychological unease:1.3)',
                            '(full body shot:1.4),(isolation in frame:1.3)',
                            '(medium shot:1.4),(waist up:1.4),(cinematic framing:1.3)',
                            '(over shoulder angle:1.4),(voyeur framing:1.3)',
                            '(floor level shot:1.4),(vulnerability framing:1.3)',
                            '(overhead shot:1.4),(from directly above:1.4),(trapped framing:1.3)',
                        ],
                    }
                    _rc2_pool = _RC2_POOLS.get(_rc2_phase, _RC2_POOLS['generic'])
                    _rc2_pick = _rc2_rand.choice(_rc2_pool)
                    wf['6']['inputs']['text'] = _rc2_pick + ',' + _rc2_pos.lstrip(', ')
                    print(f'[RAPE_COMP_V2_R] phase={_rc2_phase} pick={_rc2_pick}', flush=True)
        except Exception as _rc2_e:
            print(f'[RAPE_COMP_V2_R] err: {_rc2_e}', flush=True)

'''

new_content = content[:insert_after] + RAPE_COMP_CODE + content[insert_after:]

# 構文チェック
import tempfile, os, subprocess
tmp = tempfile.mktemp(suffix='.py')
with open(tmp, 'w', encoding='utf-8') as f:
    f.write(new_content)

result = subprocess.run(
    [r'C:\Users\fyone\anaconda3\python.exe', '-m', 'py_compile', tmp],
    capture_output=True, text=True
)
if result.returncode != 0:
    print('SYNTAX ERROR:', result.stderr)
    os.remove(tmp)
    sys.exit(1)
os.remove(tmp)
print('構文OK')

with open(r'C:\AI\ComfyUI\api_server_3001.py', 'w', encoding='utf-8') as f:
    f.write(new_content)
print('書き込み完了')
