import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
markers = ['QR_AERITH', 'AERITH_CP', 'REAL_BOOST_AERITH']
for i, l in enumerate(lines):
    for m in markers:
        if m in l:
            print(f'L{i+1}: {l.rstrip()[:150]}')
            break
