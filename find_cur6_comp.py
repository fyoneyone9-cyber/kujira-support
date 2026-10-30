import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if i < 42800: continue
    if i >= 43255: break
    if '_cur6_comp' in l:
        print(f'L{i+1}: {l.rstrip()[:200]}')
