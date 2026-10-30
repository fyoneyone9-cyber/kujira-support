import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

for i, l in enumerate(lines, 1):
    if 'DUO_POS_INJECT' in l or ('two girls' in l and 'inject' in l.lower()):
        print(f'{i}: {l}', end='')
        for j in range(i, min(len(lines), i+15)):
            print(f'  {j+1}: {lines[j]}', end='')
        print()
        break
