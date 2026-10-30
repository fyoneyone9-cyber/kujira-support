import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'moody' in l.lower() and ('_v70' in l.lower() or 'v70' in l.lower() or 'weekend' in l.lower() or 'ckpt' in l.lower() or 'checkpoint' in l.lower() or 'alias' in l.lower()):
        print(f'L{i+1}: {l.rstrip()[:200]}')
