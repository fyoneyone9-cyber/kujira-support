import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

idx = content.find('char_rohypnol_aerith')
chunk = content[idx:idx+120000]

pairs = re.findall(r'"label"\s*:\s*"([^"]+)"[^}]{0,400}?"value"\s*:\s*"([^"]{0,600})"', chunk)
for i, (label, val) in enumerate(pairs):
    if i in (15, 16, 17, 18):
        print(f'[{i}] {label}')
        print(f'  val={val[:400]}')
        print()
