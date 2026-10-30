import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

idx = content.find('char_rohypnol_aerith')
chunk = content[idx:idx+120000]

pairs = re.findall(r'"label"\s*:\s*"([^"]+)"[^}]{0,400}?"value"\s*:\s*"([^"]{0,600})"', chunk)
print('=== S1 rohypnol 性行為シーン(index 15-22) ===')
for i, (label, val) in enumerate(pairs):
    if 15 <= i <= 22:
        has1boy = '1boy' in val
        print(f'[{i}] {label} | 1boy={has1boy}')
        print(f'  val: {val[:300]}')
        print()
