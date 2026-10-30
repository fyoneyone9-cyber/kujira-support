import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if ('age_tier' in l or 'youthful' in l or 'teenage' in l or 'young face' in l or 'young girl' in l) and ('redcraft' in l.lower() or 'inject' in l.lower() or 'pos' in l.lower() or 'wf[' in l):
        print(i, repr(l.rstrip()[:120]))
