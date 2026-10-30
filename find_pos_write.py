import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# wf['6']['inputs']['text'] への書き込みで、outfit/char_prompt/full_positive が入るところ
# + outfit_prompt / full_positive 変数がどこでwf[6]に入るか
targets = ["full_positive", "outfit_prompt", "char_prompt"]
for i, l in enumerate(lines):
    for t in targets:
        if t in l and "wf['6']" in l and 'text' in l:
            print(f'L{i+1}: {l}', end='')

# PAIPAN_SYNC_V1 付近も確認
print('\n--- PAIPAN_SYNC / full_positive overwrite ---')
for i, l in enumerate(lines):
    if 'PAIPAN_SYNC' in l or ('full_positive' in l and "wf['6']" in l and i > 49000):
        print(f'L{i+1}: {l}', end='')
