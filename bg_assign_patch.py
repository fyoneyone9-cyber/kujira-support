# -*- coding: utf-8 -*-
# BG_ASSIGN_V1: CHAR_GROUP_DEFSのbigGenre未設定436件に大分類を一括付与
import io, re, sys, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

P = r'C:\AI\ComfyUI\dashboard.html'
t = io.open(P, encoding='utf-8').read()
bak = P + '.bak_bg_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy2(P, bak)
print('backup:', bak)

i = t.find('CHAR_GROUP_DEFS = [')
e = t.find('];', i)
seg = t[i:e]

# (pattern, bigGenre) 順にマッチ。最初にマッチしたものを採用
RULES = [
    # POV
    (r'^pov_', '👁 POV'),
    # 痴漢・盗撮・パンチラ
    (r'^(chikan|train_chikan|bus_chikan|tousatsu|onsen_tousatsu|panchira|stalker|toumei)', '🚃 痴漢・盗撮・パンチラ'),
    # 風俗・水商売
    (r'^(soap|rifure|pinsaro|deliheru|kyaba|sekkya|hakohealth|lolifuzoku|zenmachin|fuzoku_seal|tokoko)', '🛁 風俗・水商売'),
    # 薬物系
    (r'^(rohypnol|kakuseizai|anesthesia|drug)', '💊 薬物・昏睡'),
    # 改造・洗脳
    (r'^(kaizo|kaizou|sennou|brainwash|rel_|chiken|nppierce|succubus_kaizou|yakuza|prisoner)', '💉 改造・洗脳'),
    # レイプ・監禁・犯罪
    (r'^(rape|kankin|yousha|slave|nikubenki|virgin|auction|haikoh|jitsufu|kiroku|class_rankou|rankou|hahako|legal$|jipo_legal|pregnant|lotory|real_onigoroshi|br$|brx|dgx)', '🔞 レイプ・犯罪'),
    # ロリ・学校・飼育系
    (r'^(youjo|shogaku|chuugaku|gakurei|kyoushi|shouni|babyreg|breedfac|groom|rinjin|lolihypapp|lolisucc|lolifairy|timestop|shuukyou|loli_yankee|hoken|jikan|shougaku_boy|zukan_all|cosplay_zukan|kiroku)', '🏫 学校・ロリ系'),
    # 触手・ファンタジー
    (r'^(tentacle|tent_|elf|normal_elf|mahou|magic_youjo|fantasy|succubus|suc_iny|chijo_virus|manga_mahou)', '🐙 触手・魔法・ファンタジー'),
    # 憑依
    (r'^(hyoi|possession)', '👻 憑依・乗っ取り'),
    # 世界系・ハーレム
    (r'^(sekai|duo2|harem|factory)', '🌍 世界系・ハーレム'),
    # アニメ・芸能・コラボ
    (r'^(kimetsu|sailor|ff$|anime_|celeb|idol_akb|cp_|legal_eva|legal_sailor|legal_ff|legal_kimetsu|chibi_moon2|heroine|lora_check)', '📺 アニメ・芸能・コラボ'),
    # 汎用キャラ
    (r'^(job|costume|situ_f|adult_f|male)', '👤 汎用キャラ'),
]

pat = re.compile(r"""\{key:\s*'([^']+)'\s*,\s*label:\s*(?:'[^']*'|"[^"]*")(.*?)\}""")
assigned = {}
def repl(m):
    key = m.group(1); rest = m.group(2)
    if 'bigGenre' in rest:
        return m.group(0)
    for rp, bg in RULES:
        if re.search(rp, key):
            assigned.setdefault(bg, []).append(key)
            return m.group(0)[:-1] + ",bigGenre:'" + bg + "'}"
    assigned.setdefault('(その他のまま)', []).append(key)
    return m.group(0)

new_seg = pat.sub(repl, seg)
t = t[:i] + new_seg + t[e:]

print('--- 割当結果 ---')
for bg, keys in assigned.items():
    print(f'{len(keys):4d}  {bg}')
rest = assigned.get('(その他のまま)', [])
if rest:
    print('その他のまま:', rest)

# version +1
m = re.search(r'name="version" content="(\d+)"', t)
if m:
    ov = m.group(1); nv = str(int(ov)+1)
    t = t.replace('content="'+ov+'"', 'content="'+nv+'"')
    print('version:', ov, '->', nv)

io.open(P, 'w', encoding='utf-8').write(t)
print('patched OK')
