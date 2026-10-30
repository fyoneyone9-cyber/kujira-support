import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

hits = []
for i, l in enumerate(lines, 1):
    if 'outfit_index' in l:
        hits.append((i, l.rstrip()[:160]))

print(f'Total: {len(hits)}')
for i, l in hits[:40]:
    print(i, repr(l))
