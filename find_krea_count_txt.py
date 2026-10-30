import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if '_krea_count_txt' in l and ('=' in l) and 9600 < i < 9635:
        print(f'{i}: {l}', end='')
