# -*- coding: utf-8 -*-
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')

# api_server_3001.py でdashboard.htmlをどこから読んでいるか
with open(r'C:\AI\ComfyUI\api_server_3001.py','r',encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'dashboard' in l.lower() and ('open(' in l or 'read(' in l or 'path' in l.lower() or 'serve' in l.lower()):
        print(f'L{i+1}: {l.rstrip()[:120]}')
