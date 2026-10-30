import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# char_rape_ の CHAR_GROUP_DEFS エントリを探す
for kw in ['char_rape_ff', 'char_rape_legal_ff', "key:'rape", 'key: "rape']:
    idx = content.find(kw)
    if idx > 0:
        print(f'=== {kw} at {idx} ===')
        print(content[idx-30:idx+300])
        print()

# registerGenre で rape が登録されているか
for m in re.finditer(r"registerGenre\([^)]{0,300}\)", content):
    if 'rape' in m.group().lower():
        print('registerGenre rape:', m.group()[:300])
