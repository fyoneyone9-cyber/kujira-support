import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# L40217〜L41698の間でreturnやraiseがある箇所
for i, l in enumerate(lines):
    if i < 40216: continue
    if i > 41697: break
    stripped = l.lstrip()
    indent = len(l) - len(l.lstrip())
    if indent <= 12 and (stripped.startswith('return ') or stripped.startswith('raise ') or stripped == 'return\n'):
        print(f'L{i+1} indent={indent}: {l.rstrip()[:200]}')
