import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 全形式で探す
for cid in ['char_rape30_ff_tifa', 'char_rape30_ff_aerith', 'char_rape_legal_ff_tifa', 'char_rape_legal_ff_aerith']:
    for q in [f'"{cid}"', f"'{cid}'"]:
        idx = content.find(q)
        if idx >= 0:
            chunk = content[idx:idx+600]
            pm = re.search(r'prompt[:\s]*["\']([^"\']{0,200})', chunk)
            print(f'{cid}: pos={idx}')
            print(f'  {chunk[:300]}')
            print()
            break
    else:
        print(f'{cid}: NOT FOUND')
