import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

idx = content.find('char_rohypnol_aerith')
chunk = content[idx:idx+120000]

pairs = re.findall(r'"label"\s*:\s*"([^"]+)"[^}]{0,400}?"value"\s*:\s*"([^"]{0,400})"', chunk)
print(f'total: {len(pairs)}')
for i, (label, val) in enumerate(pairs):
    if i >= 30:
        break
    sex_hint = ''
    vl = val.lower()
    if any(k in vl for k in ['penetrat','penis','missionary','thrust','insertion','挿入','creampie','sex','1boy']):
        sex_hint = ' ← SEX'
    print(f'[{i:02d}] {label[:50]}{sex_hint}')
    if sex_hint or i >= 14:
        print(f'      {val[:180]}')
