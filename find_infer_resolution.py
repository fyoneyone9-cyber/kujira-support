import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def infer_resolution' in l:
        print(f'L{i+1}: {l}', end='')
        for j in range(i+1, min(i+80, len(lines))):
            print(f'L{j+1}: {lines[j]}', end='')
            if lines[j].strip().startswith('def ') and j > i+1:
                break
        break
