# -*- coding: utf-8 -*-
# JSエラー箇所（24412行目付近）の前後を確認
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
lines = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read().split('\n')
print('total lines:', len(lines))
for i in range(24395, 24425):
    print(i+1, repr(lines[i])[:160])
