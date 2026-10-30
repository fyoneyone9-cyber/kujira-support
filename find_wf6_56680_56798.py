import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py',encoding='utf-8',errors='replace') as f:
    lines=f.readlines()
for i,l in enumerate(lines):
    if i < 56679: continue
    if i > 56798: break
    if 'wf["6"]' in l and 'inputs' in l and 'text' in l:
        print(f'L{i+1}: {l.rstrip()[:200]}')
