import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
start = end = po = None
for i, l in enumerate(lines):
    if '# [RAPE_COMP_V3_FINAL 2026-10-21]' in l and start is None:
        start = i
    if start and i > start and '_payload_r = {"prompt": wf' in l and end is None:
        end = i
    if '# ===== PROMPT_ORDER_V1' in l and po is None:
        po = i
print(f'RAPE_COMP_V3: start=L{start+1} end(payload_r)=L{end+1}')
print(f'PROMPT_ORDER_V1: L{po+1}')
