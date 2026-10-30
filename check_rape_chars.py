import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

ids = re.findall(r"id:\s*'(char_rape[^']+)'", content)
unique = sorted(set(ids))
print(f'レイプキャラ計 {len(unique)} 体:')
for i in unique:
    print(' ', i)

# donor となるキャラのoutfits数を確認
donor = 'char_rape_jk_A'
idx = content.find(f"id: '{donor}'")
if idx > 0:
    chunk = content[idx:idx+80000]
    labels = re.findall(r'"label"\s*:\s*"([^"]+)"', chunk)
    print(f'\n{donor} outfits: {len(labels)} シーン')
    for i, l in enumerate(labels[:5]):
        print(f'  [{i}] {l}')
    print('  ...')
    for i, l in enumerate(labels[-3:]):
        print(f'  [{len(labels)-3+i}] {l}')
