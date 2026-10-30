# -*- coding: utf-8 -*-
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
DB = r'C:\AI\ComfyUI\dashboard.html'
s = open(DB, encoding='utf-8').read()
m = re.search(r'name="version" content="(\d+)"', s)
old = m.group(1); new = str(int(old) + 1)
s = s.replace('content="%s"' % old, 'content="%s"' % new, 1)
open(DB, 'w', encoding='utf-8', newline='').write(s)
print('version:', old, '->', new)
