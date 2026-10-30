import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py',encoding='utf-8',errors='replace') as f:
    lines=f.readlines()
for i,l in enumerate(lines):
    if 'as _pp' in l or ('_pp =' in l and 'import' in l):
        print(f'L{i+1}: {l.rstrip()[:150]}')
