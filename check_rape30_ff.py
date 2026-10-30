import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

for cid in ['char_rape30_ff_tifa', 'char_rape30_ff_aerith']:
    idx = content.find(f"id: '{cid}'")
    if idx < 0:
        print(f'{cid}: NOT FOUND')
        continue
    chunk = content[idx:idx+2000]
    # prompt抽出
    pm = re.search(r"prompt:\s*'([^']+)'", chunk)
    lm = re.search(r"label:\s*'([^']+)'", chunk)
    print(f'{cid}:')
    print(f'  label: {lm.group(1) if lm else "-"}')
    print(f'  prompt: {pm.group(1)[:200] if pm else "-"}')
    print()
