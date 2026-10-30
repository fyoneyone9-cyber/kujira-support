import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

idx = content.find("'char_rape_jk_A'")
chunk = content[idx:idx+200000]
labels = re.findall(r'"label"\s*:\s*"([^"]+)"', chunk)[:96]

print(f'全{len(labels)}シーン:\n')
for i, l in enumerate(labels):
    print(f'[{i:02d}] {l}')
