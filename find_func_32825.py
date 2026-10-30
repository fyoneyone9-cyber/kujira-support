import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# L32825が属する関数を探す（def で始まる最も近い行）
for i in range(32824, -1, -1):
    l = lines[i]
    if l.startswith('def ') or l.startswith('async def '):
        print(f'L{i+1}: {l.rstrip()[:150]}')
        break
