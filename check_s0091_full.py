import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\outfit_sets.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

s = data.get('S0091', [])
print(f'S0091: {len(s)}エントリ')
for i, o in enumerate(s):
    print(f'[{i}] {o}')
