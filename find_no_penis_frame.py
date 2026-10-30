import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if 'no penis in frame' in l.lower() or 'female anatomy only' in l.lower() or 'no male body parts' in l.lower():
        print(f'{i}: {l}', end='')
