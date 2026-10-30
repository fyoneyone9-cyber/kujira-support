import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# _rc3_is_rape の定義を探す
for i, l in enumerate(lines):
    if '_rc3_is_rape' in l:
        print(f'L{i+1}: {l}', end='')
