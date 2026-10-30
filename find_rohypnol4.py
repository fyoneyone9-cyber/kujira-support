import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

hits = []
for i, l in enumerate(lines, 1):
    if 'rohypnol' in l.lower():
        hits.append((i, l.rstrip()[:150]))

print(f'Total: {len(hits)} lines')
for i, l in hits[:30]:
    print(i, repr(l))
