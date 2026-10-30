import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# male判定キーワードとKREA2_NONSEX_FIX_V1の条件を探す
for i, l in enumerate(lines, 1):
    if 'SEX_COHERENCE' in l or 'KREA2_NONSEX_FIX' in l or '_is_male' in l or 'male_scene' in l:
        if 'forced oral' in l.lower() or 'penis forced' in l.lower() or 'throat' in l.lower() or 'def ' in l:
            print(i, repr(l.rstrip()[:130]))
# forced oral / throat penetration をmale判定するキーワードに含むか確認
print('\n=== male判定KWSにforced oral/throat/irrumatio があるか ===')
for i, l in enumerate(lines, 1):
    ll = l.lower()
    if ('forced oral' in ll or 'irrumatio' in ll or 'throat penetration' in ll) and ('male' in ll or 'sex' in ll):
        print(i, repr(l.rstrip()[:140]))
