import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# SEX_STATE_V1 のキーワードリストを探す
for i, l in enumerate(lines, 1):
    if 'SEX_STATE_V1' in l or ('_sx_foreplay' in l) or ('foreplay' in l and '_sx' in l):
        print(f'{i}: {l}', end='')
