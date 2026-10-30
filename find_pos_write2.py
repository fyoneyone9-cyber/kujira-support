import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# wf['6']['inputs']['text'] = ... の全行
for i, l in enumerate(lines):
    if "wf['6']['inputs']['text']" in l or 'wf["6"]["inputs"]["text"]' in l:
        print(f'L{i+1}: {l.rstrip()}')
