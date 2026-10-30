import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if '_sex' in l and ('penetration' in l or 'foreplay' in l or '= "' in l) and 54000 < i < 54110:
        print(f'{i}: {l}', end='')
