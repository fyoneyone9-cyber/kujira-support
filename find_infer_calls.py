import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# infer_resolution の全呼び出し位置と、その前後の構図注入位置を確認
infer_lines = []
comp_lines = []
for i, l in enumerate(lines):
    if 'infer_resolution(' in l:
        infer_lines.append(i+1)
    if any(k in l for k in ['RAPE_COMP_V1', 'REDCRAFT_COMPOSITION_V3', 'COMP_V3', '_rc3_pick', 'wf_blocks_fired']):
        comp_lines.append((i+1, l.strip()[:80]))

print('infer_resolution 呼び出し行:')
for ln in infer_lines:
    print(f'  L{ln}')

print('\n構図注入関連行(抜粋):')
for ln, txt in comp_lines[:15]:
    print(f'  L{ln}: {txt}')
