import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# S0091 参照をすべて出す
for m in re.finditer(r'S0091', content):
    pos = m.start()
    snippet = content[pos-100:pos+300]
    print(f'pos={pos}:')
    print(snippet)
    print('---')

# outfit_sets ローダーのロジック確認
idx = content.find('OUTFIT_SETS_LOADER')
print(f'\nOUTFIT_SETS_LOADER pos={idx}')
print(content[idx:idx+800])
