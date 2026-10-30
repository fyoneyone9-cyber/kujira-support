import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if '_qr' in l and ('import' in l or '= ' in l) and 'quality' in l.lower():
        print(f'L{i+1}: {l.rstrip()[:150]}')
