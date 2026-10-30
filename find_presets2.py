# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    c = f.read()
# AOM3とmajicを含む<option>タグを全部表示
for m in re.finditer(r'<option[^>]*>[^<]*(AOM3|majic)[^<]*</option>', c, re.IGNORECASE):
    print(repr(m.group()))
