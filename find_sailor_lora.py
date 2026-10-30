import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'sailor_lora' in l or 'is_sailor' in l or 'sailor_moon' in l.lower():
        print(f'L{i+1}: {l}', end='')
