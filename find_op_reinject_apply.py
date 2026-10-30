import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# op_reinjectをwf["6"]に書き込んでいる箇所
for i, l in enumerate(lines, 1):
    if '_op_reinject' in l and ('wf' in l or 'pos' in l.lower()) and '=' in l:
        if 'dbg' not in l and 'print' not in l and 'str(' not in l and 'get(' not in l:
            print(f'{i}: {l}', end='')
