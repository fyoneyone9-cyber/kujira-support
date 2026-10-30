import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# L49070〜L49222の間でwfを別の値に代入している箇所
for i, l in enumerate(lines):
    if i < 49069: continue
    if i > 49222: break
    if ('wf =' in l or 'wf=' in l) and 'wf["' not in l and 'wf.get' not in l and '#' not in l.lstrip()[:2]:
        print(f'L{i+1}: {l.rstrip()[:200]}')
    if 'wf["6"]' in l and 'inputs' in l and 'text' in l:
        print(f'L{i+1}: {l.rstrip()[:200]}')
