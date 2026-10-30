import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'log_file' in l and ('def ' in l or 'route' in l or '@app' in l or 'idx' in l):
        print(f'L{i+1}: {l.rstrip()}')
