# -*- coding: utf-8 -*-
import io, re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
P = r'C:\AI\ComfyUI\dashboard.html'
t = io.open(P, encoding='utf-8').read()
blocks = []
for m in re.finditer(r'<script(?![^>]*src=)[^>]*>', t):
    s = m.end(); e = t.find('</script>', s)
    if e > s: blocks.append((s, e))
s, e = blocks[29]
js = t[s:e]
lines = js.split('\n')
# 周辺コンテキスト: 配列の開始を確認
print('--- 1570-1590 ---')
for i in range(1569, 1590):
    print(i+1, repr(lines[i][:120]))
