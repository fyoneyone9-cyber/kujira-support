import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# jk_A の outfits を探す
idx = content.find('"id": "char_jk_A"')
if idx < 0:
    idx = content.find("id: 'char_jk_A'")
if idx < 0:
    idx = content.find('char_jk_A')

print(f'jk_A pos={idx}')
chunk = content[idx:idx+100000]

pairs = re.findall(r'"label"\s*:\s*"([^"]+)"[^}]{0,400}?"value"\s*:\s*"([^"]{0,400})"', chunk)
print(f'total: {len(pairs)}')
for i, (label, val) in enumerate(pairs):
    if i >= 30:
        break
    sex_hint = ''
    vl = val.lower()
    if any(k in vl for k in ['penetrat','penis','missionary','thrust','insertion','creampie','sex','1boy','doggy','cowgirl','anal']):
        sex_hint = ' ← SEX'
    print(f'[{i:02d}] {label[:60]}{sex_hint}')
    if i >= 15 or sex_hint:
        print(f'      val: {val[:200]}')
