# -*- coding: utf-8 -*-
# 孤立';'の手前の実コード行を確認（空白行をスキップして前方50行の非空行を表示）
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
lines = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read().split('\n')
center = 415362 - 1  # 0-index of '  ;'
shown = 0
i = center - 1
buf = []
while i > 0 and shown < 12:
    if lines[i].strip():
        buf.append((i+1, lines[i]))
        shown += 1
    i -= 1
for ln, txt in reversed(buf):
    print(ln, repr(txt)[:170])
print('>>>', 415362, repr(lines[center]))
