# -*- coding: utf-8 -*-
# char_jk_s1_ が他のグループ定義（JKシリーズ等）に属していないか確認
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
# char_jk を参照するGD定義を全部出す
for m in re.finditer(r"key:\s*'([^']+)',\s*label:\s*[\"']([^\"']+)[\"'][^\n]{0,60}(?:fn|match|pattern)[^\n]{0,160}char_jk[^\n]{0,80}", s):
    print(m.group(0)[:280].replace('\n','\\n'))
    print('---')
