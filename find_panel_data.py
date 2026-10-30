import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if '_panel_data' in l and ('=' in l) and 22800 < i < 22900:
        print(f'{i}: {l}', end='')
