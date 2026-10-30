import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# width/height への代入（=で設定している箇所）を探す
for i, l in enumerate(lines):
    ls = l.strip()
    if re.search(r'(width|height)\s*=\s*\d{3,4}', ls) or \
       re.search(r'"width"\s*:\s*\d{3,4}', ls) or \
       re.search(r'"height"\s*:\s*\d{3,4}', ls):
        # サイズ設定っぽい行のみ
        if not any(k in ls for k in ['stat()', 'getsize', 'KB', 'MB', 'size_']):
            print(f'L{i+1}: {l}', end='')
