import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

for cid in ['char_rape30_sailor_moon']:
    idx = content.find(f"'{cid}'")
    if idx < 0: idx = content.find(f'"{cid}"')
    chunk = content[idx:idx+800]
    print(chunk)
