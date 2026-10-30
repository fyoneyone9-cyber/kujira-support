import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# SEX_COHERENCE_V1セクション内の _sc_male / _has_positive_male 判定を探す
for i, l in enumerate(lines, 1):
    if ('_sc_male' in l or '_has_positive_male' in l or 'SEX_COHERENCE' in l) and 55900 < i < 56300:
        print(f'{i}: {l}', end='')
