import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# char_rohypnol_aerith (S1) を探す
idx = content.find('"id": "char_rohypnol_aerith"')
if idx < 0:
    idx = content.find("'id': 'char_rohypnol_aerith'")
if idx < 0:
    # push形式で探す
    idx = content.find('id: "char_rohypnol_aerith"')
if idx < 0:
    idx = content.find("char_rohypnol_aerith")

print(f'found at pos={idx}')
chunk = content[idx:idx+120000]

pairs = re.findall(r'"label"\s*:\s*"([^"]+)"[^}]{0,400}?"value"\s*:\s*"([^"]{0,400})"', chunk)
print(f'total outfits found: {len(pairs)}')
for i, (label, val) in enumerate(pairs):
    if 15 <= i <= 19:
        print(f'index {i}: {label}')
        print(f'  val: {val[:250]}')
        print()
