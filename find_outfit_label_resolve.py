import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# outfit_label → prompt 逆引きロジックがあるか
for i, l in enumerate(lines, 1):
    if 'outfit_label' in l and ('prompt' in l or 'resolve' in l.lower()) and 22850 < i < 32700:
        print(f'{i}: {l}', end='')
