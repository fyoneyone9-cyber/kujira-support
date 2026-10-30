import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# _W_FORE の定義
for i, l in enumerate(lines, 1):
    if '_W_FORE' in l and ('lick' in l or '=' in l or 'nipple' in l):
        print(f'{i}: {l}', end='')

print('\n--- background context / medical ---')
for i, l in enumerate(lines, 1):
    if 'medical facility' in l or 'surgical equipment' in l:
        print(f'{i}: {l}', end='')
