import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# 1024x1024 や size 選択ロジックを探す
for i, l in enumerate(lines):
    if '1024' in l and ('width' in l or 'height' in l or 'size' in l.lower() or 'rape30' in l):
        print(f'L{i+1}: {l}', end='')
