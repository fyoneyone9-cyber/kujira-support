import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py',encoding='utf-8',errors='replace') as f:
    lines=f.readlines()
for i,l in enumerate(lines):
    if i < 52050: continue  # CP_BEFORE_USDU以降
    if 'RAW photo' in l or 'raw photo' in l:
        print(f'L{i+1}: {l.rstrip()[:150]}')
