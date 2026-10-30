import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# L53382以降でrequests.postを探す
for i, l in enumerate(lines):
    if i < 53382: continue
    if 'requests' in l and 'post' in l.lower() and '8188' in l:
        print(f'L{i+1}: {l.rstrip()[:120]}')
    if '_payload_r' in l and 'prompt' in l and '{' in l:
        print(f'L{i+1}: {l.rstrip()[:100]}')
