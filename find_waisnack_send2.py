import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# waisnack_real ルートラベルを探す
for i, l in enumerate(lines):
    if 'waisnack_real' in l:
        print(f'L{i+1}: {l.rstrip()}')
