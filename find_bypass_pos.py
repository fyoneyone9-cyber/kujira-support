import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# L41698より前でbypass_posを定義している箇所
for i, l in enumerate(lines):
    if i >= 41698: break
    if '_bypass_pos' in l and '=' in l and '#' not in l.lstrip()[:2]:
        print(f'L{i+1}: {l.rstrip()[:200]}')
