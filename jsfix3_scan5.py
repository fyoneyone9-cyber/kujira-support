# -*- coding: utf-8 -*-
# block25を抽出し、文字列/テンプレート考慮の括弧カウンタで不一致位置を特定
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
src = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
blocks = []
for m in re.finditer(r'<script(?:\s[^>]*)?>(.*?)</script>', src, re.DOTALL):
    if len(m.group(1).strip()) >= 10:
        blocks.append((m.start(), m.group(1)))
pos, body = blocks[25]
print('block25 html line', src[:pos].count('\n')+1, 'len', len(body))
depth_p = 0
depth_b = 0
in_str = None
esc = False
i = 0
neg_events = []
while i < len(body):
    c = body[i]
    if esc:
        esc = False
    elif c == '\\':
        esc = True
    elif in_str:
        if c == in_str:
            in_str = None
    elif c in ('"', "'", '`'):
        in_str = c
    elif c == '(':
        depth_p += 1
    elif c == ')':
        depth_p -= 1
        if depth_p < 0:
            neg_events.append(('paren', i, body[:i].count('\n')+1))
            depth_p = 0
    elif c == '{':
        depth_b += 1
    elif c == '}':
        depth_b -= 1
        if depth_b < 0:
            neg_events.append(('brace', i, body[:i].count('\n')+1))
            depth_b = 0
    i += 1
print('final depth paren', depth_p, 'brace', depth_b)
print('negative events:', neg_events[:5])
for kind, off, line in neg_events[:3]:
    print('===', kind, 'js line', line)
    print(repr(body[max(0,off-300):off+80])[-450:])
