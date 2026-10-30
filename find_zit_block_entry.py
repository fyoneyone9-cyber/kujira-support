import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# L37772より前にある、ZITブロックの開始if条件を探す
for i in range(37771, -1, -1):
    l = lines[i]
    stripped = l.lstrip()
    indent = len(l) - len(stripped)
    if indent <= 8 and ('if ' in stripped or 'elif ' in stripped or 'else:' in stripped):
        print(f'L{i+1}: {l.rstrip()[:200]}')
        if i < 37600:
            break
