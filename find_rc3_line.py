import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'REDCRAFT_COMPOSITION_V3' in l or '_rc3_pick' in l or 'RAPE_COMP_V1' in l:
        print(f'L{i+1}: {l.rstrip()}')
