# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    content = f.read()
    lines = content.splitlines(keepends=True)

m = re.search(r"name=['\"]version['\"] content=['\"](\d+)['\"]", content)
print('version:', m.group(1) if m else '?')

l = lines[24685]
print('L24686 len:', len(l))
print('col1330-1420:', l[1330:1420])

legal_count = content.count("'legal':")
print('legal count:', legal_count)

# L24686内の全キーを抽出
keys = re.findall(r"'([^']+)':", l)
print('all keys in L24686:', keys[:40])
