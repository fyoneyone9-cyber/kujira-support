"""
医療改造キャラを30シーンに拡張し、甘露寺蜜璃・レイ・アスカを追加する
"""
import re, sys, json, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')

DASHBOARD = r'C:\AI\ComfyUI\dashboard.html'

# 30シーン定義（全キャラ共通）
OUTFITS_30 = [
    {"label": "01「麻酔が効かない…動けないのに、全部わかる」手術台に縛られ局所麻酔だけで切開される恐怖", "value": "(operating table:2.0),(medical restraints:1.9),(scalpel:1.8),(surgical incision:1.8),(conscious during surgery:1.9),(terror:1.8),(tears streaming:1.7),(hospital gown torn open:1.7),(surgical lights overhead:1.6),(helpless:1.8)"},
    {"label": "02「なんで…なんでそこを切るの」メスが粘膜に触れた瞬間、声にならない悲鳴", "value": "(scalpel touching sensitive tissue:2.0),(silent scream:1.9),(wide eyes in horror:1.8),(operating room:1.7),(body restrained:1.8),(surgical gloves:1.6),(medical tools:1.7),(tears:1.8),(desperate expression:1.9),(hospital:1.6)"},
    {"label": "03「縫われてる…自分の体が縫われてる」意識がある中、縫合される感触と絶望", "value": "(suturing:2.0),(conscious:1.9),(surgical needle and thread:1.8),(despair:1.8),(operating room:1.7),(body modification:1.7),(tears:1.7),(trembling:1.6),(medical procedure:1.8),(horror expression:1.8)"},
    {"label": "04「目が覚めたら…もう元に戻れない体になってた」術後包帯の下の自分の体を知る瞬間", "value": "(post-surgery:2.0),(bandaged body:1.9),(waking up:1.7),(hospital bed:1.8),(looking down at body:1.7),(horror realization:1.9),(modified body:1.8),(white bandages:1.7),(despair:1.8),(alone in hospital room:1.6)"},
    {"label": "05「鏡を…見せないで」術後の全身鏡、改造された自分の体との初対面", "value": "(full body mirror:2.0),(post-surgery body:1.9),(body modification visible:1.8),(horror:1.8),(covering face:1.7),(surgical scars:1.8),(hospital gown:1.6),(breakdown:1.8),(tears:1.7),(refusing to look:1.7)"},
    {"label": "06「傷跡が…消えない。ずっとここに残る」消えない縫合跡を指でなぞる絶望の夜", "value": "(surgical scars:2.0),(tracing scars with finger:1.9),(night in hospital:1.7),(despair:1.8),(modified body:1.8),(lingering trauma:1.7),(tears:1.7),(dim lighting:1.6),(alone:1.7),(permanent marks:1.8)"},
    {"label": "07「助けて…誰か助けて」何週間も経った今も夜中に泣く。改造された体で生きていく絶望", "value": "(crying alone at night:2.0),(modified body:1.9),(weeks after surgery:1.7),(PTSD:1.7),(hospital room:1.6),(hugging knees:1.8),(tears:1.8),(trembling:1.7),(no escape:1.8),(despair:1.9)"},
    {"label": "08「また…来るの」定期検診と称して繰り返される改造処置への恐怖", "value": "(medical examination:2.0),(returning to operating room:1.9),(terror:1.8),(doctor approaching:1.7),(restraints:1.7),(modified body:1.8),(whimpering:1.7),(hospital:1.7),(repeated procedures:1.8),(helpless:1.8)"},
    {"label": "09「体の中に…何かを入れられた」異物埋め込み処置の最中の感覚", "value": "(implant surgery:2.0),(foreign object inserted:1.9),(surgical procedure:1.8),(terror:1.8),(body modification surgery:1.9),(operating table:1.7),(tears:1.8),(conscious:1.7),(medical instruments:1.7),(horror:1.8)"},
    {"label": "10「薬で…意識が遠くなっていく」鎮静剤で朦朧とする中、処置が続く", "value": "(sedated:2.0),(hazy consciousness:1.9),(medical drugs administered:1.8),(operating room:1.7),(blurry vision:1.8),(body being modified:1.7),(helpless:1.8),(IV drip:1.7),(dazed expression:1.8),(hospital:1.6)"},
    {"label": "11「声が出せない…口に管が入ってる」気管挿管された状態での無力感", "value": "(intubated:2.0),(breathing tube:1.9),(unable to speak:1.8),(medical procedure:1.8),(tears flowing:1.7),(restrained on table:1.8),(monitor beeping:1.6),(surgical team:1.6),(terror:1.8),(helpless:1.9)"},
    {"label": "12「体が…誰かのものになってしまった」改造完了後、所有物として扱われる", "value": "(post-modification:2.0),(treated as property:1.9),(modified body displayed:1.8),(shame:1.8),(objectified:1.9),(medical setting:1.6),(inspected by doctor:1.7),(marks on body:1.8),(humiliation:1.8),(despair:1.7)"},
    {"label": "13「痛みに慣れさせられていく…」繰り返される処置で感覚が麻痺していく", "value": "(repeated medical procedures:2.0),(pain conditioning:1.9),(numb expression:1.8),(hospital:1.7),(surgical scars multiple:1.8),(broken will:1.8),(dissociation:1.7),(operating room:1.7),(modified body:1.8),(empty eyes:1.8)"},
    {"label": "14「誰にも言えない…見せられない体」傷跡を隠して普通の生活を送る苦しさ", "value": "(hiding scars under clothing:2.0),(public setting:1.7),(modified body hidden:1.8),(internal despair:1.8),(school uniform:1.6),(smiling facade:1.7),(trauma concealed:1.8),(surgical marks:1.7),(isolated:1.7),(secret pain:1.8)"},
    {"label": "15「なぜ私だけ…」同年代の子と自分の体を比べてしまう瞬間", "value": "(comparing bodies:1.9),(locker room:1.7),(surgical scars visible:1.8),(shame:1.8),(jealousy and despair:1.7),(modified body:1.8),(covering up:1.7),(tears:1.7),(isolation:1.8),(why me:1.8)"},
    {"label": "16「先生に…またベッドに連れて行かれる」信頼していた人物からの裏切り", "value": "(betrayal:2.0),(doctor leading to procedure room:1.9),(fear:1.8),(medical setting:1.7),(forced:1.8),(modified body:1.7),(despair:1.8),(resistance:1.7),(alone with authority figure:1.8),(trauma:1.8)"},
    {"label": "17「麻酔が切れてきた…なのに処置が続いてる」痛みの中での処置継続", "value": "(anesthesia wearing off:2.0),(procedure continuing:1.9),(pain:1.8),(tears:1.8),(operating room:1.7),(helpless:1.8),(medical team ignoring pain:1.7),(restrained:1.8),(agony:1.9),(surgical lights:1.6)"},
    {"label": "18「採取されてる…自分の体から何かが」生体サンプル採取の恐怖", "value": "(biological sample collection:2.0),(medical extraction:1.9),(terrified:1.8),(hospital:1.7),(body violated:1.8),(medical instruments:1.7),(tears:1.8),(helpless:1.7),(lab setting:1.6),(modified body:1.7)"},
    {"label": "19「モルモットみたいに…」実験台として繰り返し検査される", "value": "(medical experiment subject:2.0),(repeated examinations:1.9),(test subject:1.8),(lab:1.7),(measured and documented:1.7),(degraded:1.8),(modified body examined:1.8),(clinical setting:1.7),(objectified:1.8),(despair:1.8)"},
    {"label": "20「写真を撮られてる…記録として」改造後の体を記録・撮影される屈辱", "value": "(being photographed:2.0),(medical documentation:1.9),(modified body recorded:1.8),(shame:1.8),(clinical photography:1.7),(exposed:1.8),(humiliation:1.8),(hospital:1.7),(objectified:1.8),(despair:1.7)"},
    {"label": "21「改造された部分が…疼く」処置後も続く異様な感覚", "value": "(post-modification sensation:2.0),(aching implants:1.9),(modified body:1.8),(confusion:1.7),(touching modification site:1.8),(hospital room:1.6),(unsettling feeling:1.8),(physical trauma:1.7),(alone:1.7),(disturbed:1.8)"},
    {"label": "22「次はどこを…変えられるの」次の処置への恐怖と不安", "value": "(anticipating next procedure:2.0),(dread:1.9),(modified body:1.8),(hospital:1.7),(waiting:1.8),(fear of unknown:1.8),(hugging self:1.7),(tears:1.7),(medical setting:1.6),(helpless:1.8)"},
    {"label": "23「逃げたい…でも体が動かない」拘束からの脱出を試みる無力感", "value": "(attempting escape:2.0),(restrained:1.9),(medical restraints:1.8),(operating table:1.7),(struggling:1.8),(tears:1.8),(modified body:1.7),(terror:1.8),(trapped:1.9),(despair:1.8)"},
    {"label": "24「外は…普通の世界なのに」病室の窓から見える外の世界との断絶感", "value": "(looking out hospital window:2.0),(longing:1.8),(modified body:1.8),(isolation:1.8),(normal world outside:1.7),(hospital room:1.7),(despair:1.8),(tears:1.7),(trapped:1.8),(window light:1.6)"},
    {"label": "25「誰かに見つけてほしい…でも見られたくない」矛盾した感情", "value": "(conflicted emotions:2.0),(hiding modified body:1.8),(longing for rescue:1.8),(shame:1.8),(alone:1.7),(hospital corridor:1.6),(tears:1.7),(covering scars:1.7),(desperate:1.8),(isolation:1.8)"},
    {"label": "26「元の体に…戻れるの？」改造の可逆性への絶望", "value": "(questioning reversal:2.0),(hopeless:1.9),(modified body:1.8),(doctor consultation:1.7),(despair:1.8),(tears:1.7),(permanent modification:1.8),(medical setting:1.6),(broken hope:1.8),(alone:1.7)"},
    {"label": "27「今日も…検査」日常化した医療行為への感覚麻痺", "value": "(routine medical examination:2.0),(numb:1.9),(dissociated:1.8),(hospital:1.7),(modified body:1.8),(empty eyes:1.8),(compliance:1.7),(repeated trauma:1.8),(clinical setting:1.7),(broken spirit:1.8)"},
    {"label": "28「体を…売られる」実験体として他機関に引き渡される恐怖", "value": "(being transferred:2.0),(sold as experiment:1.9),(terror:1.8),(modified body:1.8),(transported:1.7),(new facility:1.7),(despair:1.9),(helpless:1.8),(medical setting:1.6),(no escape:1.8)"},
    {"label": "29「この体で…生きていける？」改造後の人生への絶望と諦め", "value": "(facing new reality:2.0),(modified body:1.9),(life after surgery:1.7),(despair:1.8),(looking at hands:1.7),(broken:1.8),(tears:1.7),(alone:1.7),(acceptance of horror:1.8),(hopeless:1.8)"},
    {"label": "30「もう…何も感じなくなった」完全に心が折れた最終段階", "value": "(completely broken:2.0),(empty expression:1.9),(modified body:1.8),(dissociation:1.8),(hospital:1.7),(dead eyes:1.9),(no more tears:1.7),(sitting still:1.7),(surrendered:1.8),(final despair:1.9)"},
]

# 新キャラ定義
NEW_CHARS = [
    {
        "id": "char_kaizou_med_mitsuri",
        "genre": "医療改造",
        "label": "💉 医療改造・鬼滅・甘露寺蜜璃",
        "gender": "female",
        "age": "young_adult",
        "prompt": "Kanroji Mitsuri,Kimetsu no Yaiba,pink hair with green tips,long hair,large breasts,voluptuous body,green eyes,beauty mark under left eye,Demon Slayer Corps uniform,japanese girl,anime style",
        "neg": "male,boy,ugly,deformed,extra limbs,bad anatomy,watermark",
        "patterns_ref": "S0093",
    },
    {
        "id": "char_kaizou_med_rei",
        "genre": "医療改造",
        "label": "💉 医療改造・セーラーマーズ・火野レイ",
        "gender": "female",
        "age": "jk",
        "prompt": "Hino Rei,Sailor Mars,black long hair,purple eyes,slender,japanese shrine maiden,Sailor Moon character,red and purple sailor uniform,serious expression,anime style",
        "neg": "male,boy,ugly,deformed,extra limbs,bad anatomy,watermark",
        "patterns_ref": "S0093",
    },
    {
        "id": "char_kaizou_med_asuka",
        "genre": "医療改造",
        "label": "💉 医療改造・エヴァ・惣流アスカ",
        "gender": "female",
        "age": "jk",
        "prompt": "Asuka Langley Soryu,Neon Genesis Evangelion,fiery red hair,twin braids,blue eyes,strong personality,plugsuit,14 years old,slender,anime style",
        "neg": "male,boy,ugly,deformed,extra limbs,bad anatomy,watermark",
        "patterns_ref": "S0093",
    },
]

def obj_to_js_inline(d, outfits):
    """キャラ定義 + outfitsをインライン1行のpush形式に変換"""
    parts = {}
    for k, v in d.items():
        if k == 'patterns_ref':
            continue
        parts[k] = v
    parts['outfits'] = outfits
    # JSON形式で出力
    return 'window.CHAR_TEMPLATES.female.push(' + json.dumps(parts, ensure_ascii=False) + ');'

def update_existing_outfits(content, outfits_30):
    """既存の医療改造キャラのoutfitsを30シーンに更新"""
    lines = content.split('\n')
    updated = 0
    outfits_json = json.dumps(outfits_30, ensure_ascii=False)

    for j in range(len(lines)):
        l = lines[j]
        if 'char_kaizou_med_' not in l:
            continue
        if '"outfits":' not in l and "'outfits':" not in l:
            continue
        # outfitsを置換
        new_l = re.sub(r'"outfits":\s*\[.*?\]', '"outfits":' + outfits_json, l)
        if new_l != l:
            lines[j] = new_l
            id_m = re.search(r'"id":\s*"([^"]+)"', l)
            print(f"  Updated: {id_m.group(1) if id_m else '?'}")
            updated += 1
    return '\n'.join(lines), updated

def run():
    with open(DASHBOARD, encoding='utf-8', errors='replace') as f:
        content = f.read()

    print("=== Step1: 既存キャラのoutfitsを30シーンに更新 ===")
    content, updated = update_existing_outfits(content, OUTFITS_30)
    print(f"Updated {updated} chars")

    print("=== Step2: 新キャラ追加（mitsuri / rei / asuka） ===")
    # block22の末尾（最後の </script> 直前）に追加
    scripts_iter = list(re.finditer(r'(<script(?:\s[^>]*)?>)(.+?)(</script>)',
                                     content, re.DOTALL | re.IGNORECASE))
    sc22 = scripts_iter[22]
    insert_pos = sc22.end(2)

    new_js_parts = []
    for char in NEW_CHARS:
        js = obj_to_js_inline(char, OUTFITS_30)
        new_js_parts.append(js)
        print(f"  Prepared: {char['id']}")

    insert_text = '\n\n' + '\n\n'.join(new_js_parts) + '\n\n'
    content = content[:insert_pos] + insert_text + content[insert_pos:]

    # バージョン更新
    ver_m = re.search(r'content="(\d{10,})"', content)
    if ver_m:
        old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
        content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
        print(f"Version: {old_ver} -> {new_ver}")

    print("=== Step3: JS検証 ===")
    scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
    errors = []
    for i, sc in enumerate(scripts):
        sc2 = sc.strip()
        if not sc2 or len(sc2) < 20: continue
        tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
        tmp.write(sc2); tmp.close()
        r = subprocess.run(['node', '--check', tmp.name], capture_output=True, timeout=30)
        os.unlink(tmp.name)
        if r.returncode != 0:
            errors.append((i, r.stderr.decode('utf-8', errors='replace')))
    print(f"JS errors: {len(errors)}")
    for i, e in errors[:3]: print(f"  block{i}: {e[:200]}")

    if errors:
        print("検証失敗。保存しませんでした。")
        return

    ts = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    bak = r'C:\AI\ComfyUI\dashboard_backup_medfix_' + ts + '.html'
    shutil.copy2(DASHBOARD, bak)
    print(f"Backup: {bak}")
    with open(DASHBOARD, 'w', encoding='utf-8') as f:
        f.write(content)
    print("=== 完了 ===")
    print("次: Ctrl+Shift+R でリロード")

if __name__ == '__main__':
    run()
