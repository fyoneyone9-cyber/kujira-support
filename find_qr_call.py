import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# apply_quality_rules の呼び出し箇所を全部探す
for i, l in enumerate(lines):
    if 'apply_quality_rules' in l and ('(' in l):
        print(f'L{i+1}: {l.rstrip()}')

print()
# weight_budget の keep をいじっている箇所
for i, l in enumerate(lines):
    if 'weight_budget' in l and 'keep' in l:
        print(f'L{i+1}: {l.rstrip()}')
