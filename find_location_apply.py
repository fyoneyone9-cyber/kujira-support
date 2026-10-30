import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# _LOCATION_JP_MAP が実際に使われている箇所
for i, l in enumerate(lines, 1):
    if '_LOCATION_JP_MAP' in l:
        print(f'{i}: {l}', end='')
        # 前後5行
        for j in range(max(1,i-1), min(len(lines), i+6)):
            print(f'  {j}: {lines[j-1]}', end='')
        print()
