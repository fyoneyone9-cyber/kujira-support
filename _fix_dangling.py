# -*- coding: utf-8 -*-
import io, re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
P = r'C:\AI\ComfyUI\dashboard.html'
B = r'C:\AI\ComfyUI\dashboard.html.bak_delseason_20261027_192440'
t = io.open(P, encoding='utf-8').read()
tb = io.open(B, encoding='utf-8').read()

# block29相当を特定して該当行の前後を表示
blocks = []
for m in re.finditer(r'<script(?![^>]*src=)[^>]*>', t):
    s = m.end(); e = t.find('</script>', s)
    if e > s: blocks.append((s, e))
s, e = blocks[29]
js = t[s:e]
lines = js.split('\n')
print('=== block29 line 1585-1595 ===')
for i in range(1584, 1596):
    print(i+1, repr(lines[i][:160]))

# block32: バックアップに同じ内容があるか（既存バグ確認）
s32, e32 = blocks[32]
js32 = t[s32:e32]
print()
print('block32 preexisting in backup:', js32 in tb)
print('=== block32 head ===')
print(js32[:300])
