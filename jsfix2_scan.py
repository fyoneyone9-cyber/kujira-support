# -*- coding: utf-8 -*-
# 壊れた2ブロックの孤立 '},' 位置の前後を確認
# block5: html line 2675 + js line 414 / block21: html line 10036 + js line 14390
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
lines = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read().split('\n')
for base, js in [(2675, 414), (10036, 14390)]:
    # scriptタグ行 + js行 (jsの1行目はscriptタグ直後)
    center = base + js - 1
    print('=== around html line', center+1)
    for i in range(center-6, center+5):
        print(i+1, repr(lines[i])[:150])
