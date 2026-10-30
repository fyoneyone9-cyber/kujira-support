import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

for cid in ['char_rape_jd_A', 'char_pov_rape_jd_A']:
    idx = content.find(f"'{cid}'")
    if idx < 0: idx = content.find(f'"{cid}"')
    chunk = content[idx:idx+3000]
    
    # ラベルを全部抽出（長いvalueをまたいで）
    labels = re.findall(r'label:\s*"([^"]+)"', chunk)
    
    print(f'{cid}: {len(labels)}シーン')
    for i, l in enumerate(labels[:10]):
        print(f'  [{i}] {l}')
    if len(labels) > 10:
        print(f'  ... (+{len(labels)-10})')
    print()
