# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

l = lines[24685]
print(f'L24686 len={len(l)}')
# col1361前後（ブラウザはUTF-16単位の可能性があるので広めに）
print(f'col1340-1400: {repr(l[1340:1400])}')

# key:label パターンを全検索
broken = []
for i, line in enumerate(lines):
    if re.search(r"key:label:", line.replace(' ','').replace('\t','')):
        broken.append((i+1, line.rstrip()[:120]))
print(f'\nBroken key:label entries: {len(broken)}')
for ln, txt in broken:
    print(f'  L{ln}: {txt}')
