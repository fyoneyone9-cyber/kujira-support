import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# pov キーワード拡張
OLD_POV = "                    ('pov', ['pov','first person','looking up at','upward gaze','見上げ','上から','加害者視点','俯瞰','監視','predator pov','from above perspective','looking down at her','voyeur','watching from','observed']),"
NEW_POV = """                    ('pov', ['pov','first person','looking up at','upward gaze','見上げ','上から','加害者視点','俯瞰','監視','predator pov','from above perspective','looking down at her','voyeur','watching from','observed',
                        'close-up face','forced penetr','begging through','please stop','prolonged assault','forcing physical',
                        '最初の貫通','懇願する','強制絶頂','屈辱','貫通',
                    ]),"""

if OLD_POV in content:
    content = content.replace(OLD_POV, NEW_POV)
    print('pov拡張OK')
else:
    print('ERROR: pov old not found')
    idx = content.find("'pov', ['pov'")
    print(repr(content[idx-30:idx+100]))

# filming キーワード拡張（盗撮系・EX系をfilingに追加）
OLD_FILMING = "                    ('filming', ['撮影','記録','カメラ','証拠','写真','カメラを向け','filming','recorded','camera','photograph','on camera','being filmed','posed for','documentation','video','taking photos','snapshot','evidence photo']),"
NEW_FILMING = """                    ('filming', ['撮影','記録','カメラ','証拠','写真','カメラを向け','filming','recorded','camera','photograph','on camera','being filmed','posed for','documentation','video','taking photos','snapshot','evidence photo',
                        # 盗撮系
                        '盗-','盗撮','upskirt','スカートの中','自撮り','着替え','開脚','前かがみ','突っ伏し',
                        # EXシリーズ（転売・配信・公開陵辱等）
                        '転売','vipクライアント','公開陵辱','永続配信','次世代連鎖','繁殖プログラム',
                    ]),"""

if OLD_FILMING in content:
    content = content.replace(OLD_FILMING, NEW_FILMING)
    print('filming拡張OK')
else:
    print('ERROR: filming old not found')

# conditioning拡張（EX-催眠・洗脳強化）
OLD_COND = "                    ('conditioning', ['感度開発','調教','バイブ','週末は','ルーティン','体が慣れ','conditioning','trained','sensitivity','vibrator','brainwash','mind control','weekly routine','conditioned response','behavioral conditioning','trained to','obedient','submissive posture']),"
NEW_COND = """                    ('conditioning', ['感度開発','調教','バイブ','週末は','ルーティン','体が慣れ','conditioning','trained','sensitivity','vibrator','brainwash','mind control','weekly routine','conditioned response','behavioral conditioning','trained to','obedient','submissive posture',
                        '催眠','洗脳強化','薬物完全依存','依存','更なる監禁',
                    ]),"""

if OLD_COND in content:
    content = content.replace(OLD_COND, NEW_COND)
    print('conditioning拡張OK')
else:
    print('ERROR: conditioning old not found')

# drag拡張（脱走試み・監禁強化）
OLD_DRAG = "                    ('drag', ['引きずり','引き込','連れ込','拉致','連行','押し込','押し倒','投げ込','引っ張','部屋に','監禁部屋','dragged','grabbed','abducted','kidnap','forced into','pulled into','pushed into','being pushed','thrown into','shoved into','locked in','chain collar','首にチェーン','collar clicking','chain clicked','collar being locked','チェーンを付']),"
NEW_DRAG = """                    ('drag', ['引きずり','引き込','連れ込','拉致','連行','押し込','押し倒','投げ込','引っ張','部屋に','監禁部屋','dragged','grabbed','abducted','kidnap','forced into','pulled into','pushed into','being pushed','thrown into','shoved into','locked in','chain collar','首にチェーン','collar clicking','chain clicked','collar being locked','チェーンを付',
                        '脱走試み','监禁強化','監禁強化',
                    ]),"""

if OLD_DRAG in content:
    content = content.replace(OLD_DRAG, NEW_DRAG)
    print('drag拡張OK')
else:
    print('ERROR: drag old not found')

with open(r'C:\AI\ComfyUI\api_server_3001.py', 'w', encoding='utf-8') as f:
    f.write(content)
print('書き込み完了')
