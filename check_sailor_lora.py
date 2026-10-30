import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# _is_sailor_lora 判定ブロック全体
for i, l in enumerate(lines):
    if '_is_sailor_lora' in l:
        print(f'L{i+1}: {l.rstrip()}')
