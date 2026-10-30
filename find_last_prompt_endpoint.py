import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if 'last-prompt' in l and ('route' in l or 'app.' in l or '@' in l):
        print(f"L{i+1}: {l.rstrip()[:120]}")
        for j in range(i, min(i+10, len(lines))):
            print(f"  L{j+1}: {lines[j].rstrip()[:100]}")
        print()
