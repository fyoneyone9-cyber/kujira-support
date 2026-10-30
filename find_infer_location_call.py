import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

for i, l in enumerate(lines, 1):
    if 'infer_location' in l or ('_dlg' in l and 'char_prompt' in l):
        print(f'{i}: {l}', end='')
