import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

for i, l in enumerate(lines, 1):
    if 'outfit_index' in l and ('generateSinglePanel' in l or 'fetch' in l or 'body' in l or 'JSON' in l or 'send' in l.lower()):
        print(i, repr(l.rstrip()[:160]))
