import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
V70_PARTIAL = "v70_fp8"
V70_FULL = "moodyKrea2MixUncensoredWeekend_v70"
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if V70_PARTIAL in l or V70_FULL in l or 'v70' in l.lower():
        print(f'L{i+1}: {l.rstrip()[:150]}')
