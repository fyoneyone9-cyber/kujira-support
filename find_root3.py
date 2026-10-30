# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py','r',encoding='utf-8') as f:
    content = f.read()
# ROOT定義を探す
import re
for m in re.finditer(r'^ROOT\s*=.*', content, re.MULTILINE):
    print(f'pos={m.start()}: {m.group()[:120]}')
# dashboard.htmlへのパスを全部洗い出す
for m in re.finditer(r'["\'][^"\']*dashboard\.html[^"\']*["\']', content):
    print(f'pos={m.start()}: {m.group()[:100]}')
