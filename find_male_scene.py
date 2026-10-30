import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# _is_male_scene の代入行を探す
for i, l in enumerate(lines, 1):
    if '_is_male_scene' in l and ('=' in l) and 30000 < i < 57000:
        print(f'{i}: {l}', end='')
