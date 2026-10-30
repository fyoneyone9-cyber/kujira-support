import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'dashboard.html' in l and ('FileResponse' in l or 'HTMLResponse' in l or 'open' in l or 'serve' in l.lower() or 'static' in l.lower()):
        print(f'L{i+1}: {l.rstrip()}')
