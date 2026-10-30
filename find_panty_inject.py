import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# panties under skirt / visible panties を注入している箇所
for i, l in enumerate(lines, 1):
    if 'panties under skirt' in l or 'visible panties' in l:
        if 'inject' in l.lower() or '+=' in l or 'text' in l.lower() or 'prepend' in l.lower() or 'wf[' in l:
            print(i, repr(l.rstrip()[:120]))
