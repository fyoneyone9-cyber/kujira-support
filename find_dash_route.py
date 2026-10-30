import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# dashboard.htmlをHTMLResponseで返しているルートを探す
for i, l in enumerate(lines):
    if 'HTMLResponse' in l and ('dashboard' in l or '/' == l.strip()):
        print(f'L{i+1}: {l.rstrip()}')
    if "@app.get('/')" in l or '@app.get("/")' in l:
        print(f'L{i+1}: {l.rstrip()}')
        for j in range(i, i+15):
            print(f'L{j+1}: {lines[j].rstrip()}')
        break
