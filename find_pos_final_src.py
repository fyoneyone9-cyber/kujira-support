import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# L43534より前で_pos_finalに代入している最後の箇所
results = []
for i, l in enumerate(lines):
    if i >= 43534: break
    if i < 40000: continue
    if '_pos_final' in l and '=' in l and '#' not in l.lstrip()[:2] and '.get(' not in l:
        results.append((i+1, l.rstrip()[:200]))
# 最後の10件
for ln, l in results[-20:]:
    print(f'L{ln}: {l}')
