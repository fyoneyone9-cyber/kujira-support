import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if '_src_for_male' in l:
        print(i, repr(l.rstrip()[:140]))
