# -*- coding: utf-8 -*-
# 対象9グループのGD定義（fnパターン）とID実体を特定
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
keys = ['magic_youjo','mahou','mahou_tentacle','tentacle_mahou','tentacle_elf','mahou_shoujo','mahou_youjo','mahou_youchien','manga_mahou','tentacle','grp_manga_mahou','mahou_age','manga_mahou_jc','manga_mahou_jk','mahou_jk','mahou_shougaku','mahou_chuugaku']
for k in keys:
    for m in re.finditer(r"key:\s*'" + k + r"',\s*label:\s*[\"']([^\"']*)[\"'],\s*(?:fn|match|icon|cats)[^\n]{0,180}", s):
        print(k, '|', m.group(0)[:200].replace('\n','\\n'))
        print('---')
