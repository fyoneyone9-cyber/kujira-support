import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# _SEX_RESOLVED への代入箇所を全部出す
for i, l in enumerate(lines, 1):
    if '_SEX_RESOLVED' in l and ('=' in l) and 'if' not in l and 'print' not in l and 'get' not in l:
        print(i, repr(l.rstrip()[:120]))
