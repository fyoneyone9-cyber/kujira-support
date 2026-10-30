import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# panties under skirt を含む全行
for i, l in enumerate(lines, 1):
    if 'panties under skirt' in l:
        print(i, repr(l.rstrip()[:120]))
