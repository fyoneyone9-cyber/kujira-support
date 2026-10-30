import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if 'no pubic hair:3.0' in l or ('PAIPAN_INJECT_GLOBAL' in l and 'enforced' in l):
        print(i, repr(l.rstrip()[:130]))
