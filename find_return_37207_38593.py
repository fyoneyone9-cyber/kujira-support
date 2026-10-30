import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if i < 37207: continue
    if i >= 38592: break
    stripped = l.lstrip()
    indent = len(l) - len(stripped)
    if indent <= 8 and (stripped.startswith('return ') or stripped == 'return\n'):
        print(f'L{i+1} indent={indent}: {l.rstrip()[:200]}')
