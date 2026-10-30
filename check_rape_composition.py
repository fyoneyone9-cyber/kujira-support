import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# rape関連の構図ロジックを探す
targets = ['char_rape', 'RAPE', '_rape_', 'rape_comp', 'REDCRAFT_COMPOSITION']
found = []
for i, l in enumerate(lines):
    for t in targets:
        if t in l:
            found.append((i+1, l.rstrip()))
            break

# 重複排除して出力
seen = set()
for lineno, l in found:
    if l not in seen:
        seen.add(l)
        print(f'L{lineno}: {l[:140]}')
