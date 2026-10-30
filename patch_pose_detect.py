# -*- coding: utf-8 -*-
import shutil, datetime

src = r'C:\AI\ComfyUI\pose_presets.py'
bak = src + '.bak_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy2(src, bak)
print(f'Backup: {bak}')

with open(src, 'r', encoding='utf-8') as f:
    c = f.read()

old = '''def detect(text):
    tl = (text or "").lower()
    for p in PRESETS:
        if re.search(p["detect"], tl, re.IGNORECASE):
            return p
    return None'''

new = '''def detect(text):
    tl = (text or "").lower()
    # [LEASH_POSE_GUARD_V1 2026-10-22] leash/collar+on all fours \u306f\u8abf\u6559\u30dd\u30fc\u30ba\u3067\u3042\u308a
    # doggy sex \u3067\u306f\u306a\u3044\u3002\u6027\u884c\u70ba\u6307\u793a(\u633f\u5165\u7cfb\u30ad\u30fc\u30ef\u30fc\u30c9)\u304c\u306a\u3044\u5834\u5408\u306f doggy \u306e\u8aa4\u767a\u706b\u3092\u9632\u3050\u3002
    _leash_keywords = ['being led by leash', 'collar with leash', 'on leash', 'led by leash', 'leash pulled']
    _sex_keywords = ['penetration', 'insertion', 'sex from behind', 'doggystyle', 'doggy style',
                     '\u633f\u5165', '\u4e2d\u51fa\u3057', '\u30cf\u30e1', 'from behind sex', 'rear entry sex']
    _has_leash = any(k in tl for k in _leash_keywords)
    _has_sex = any(k in tl for k in _sex_keywords)
    for p in PRESETS:
        if re.search(p["detect"], tl, re.IGNORECASE):
            # leash\u8abf\u6559\u30b7\u30fc\u30f3\u306b\u6027\u884c\u70ba\u6307\u793a\u304c\u306a\u3044 \u2192 doggy\u7cfb\u306f\u30b9\u30ad\u30c3\u30d7
            if _has_leash and not _has_sex and p["key"] in ("doggy", "standing_doggy"):
                print("[LEASH_POSE_GUARD_V1] skip doggy detection (leash scene, no sex keyword)", flush=True)
                continue
            return p
    return None'''

if old in c:
    c = c.replace(old, new)
    print('Patched detect()')
else:
    print('ERROR: target not found')

with open(src, 'w', encoding='utf-8') as f:
    f.write(c)
print('Done')
