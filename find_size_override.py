import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# EmptyLatentImage や width/height の書き換えを探す
for i, l in enumerate(lines):
    ls = l.strip()
    if ('EmptyLatentImage' in ls or 'latent' in ls.lower()) and ('width' in ls or 'height' in ls):
        print(f'L{i+1}: {l}', end='')
    elif re.search(r'\["width"\]|wf\[.+\]\["inputs"\]\["width"\]|\["height"\]', ls):
        print(f'L{i+1}: {l}', end='')
    elif '1024' in ls and ('wf' in ls or 'inputs' in ls):
        print(f'L{i+1}: {l}', end='')
