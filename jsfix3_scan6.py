# -*- coding: utf-8 -*-
# 調査: factory push( の開始から '  );' までの構造骨格を出す（'});' で既に閉じていないか確認）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
src = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
i = src.find("id: 'char_factory_youjo_A'")
start = src.rfind('window.CHAR_TEMPLATES.female.push(', 0, i)
# ';'行の位置
lines = src.split('\n')
semi_off = sum(len(l)+1 for l in lines[:415361])
seg = src[start:semi_off+10]
print('seg len', len(seg), 'start line', src[:start].count('\n')+1)
# 構造トークンのみ抽出（文字列外の { } ( ) ; を行番号付きで）
depth_p = 0; depth_b = 0
in_str = None; esc = False
events = []
for j, c in enumerate(seg):
    if esc: esc = False; continue
    if c == '\\': esc = True; continue
    if in_str:
        if c == in_str: in_str = None
        continue
    if c in ('"', "'", '`'): in_str = c; continue
    if c in '(){};':
        line = src[:start+j].count('\n')+1
        if c == '(': depth_p += 1
        elif c == ')': depth_p -= 1
        elif c == '{': depth_b += 1
        elif c == '}': depth_b -= 1
        events.append((line, c, depth_p, depth_b))
# depth_b==0 になる } と、);・; を表示
for line, c, dp, db in events:
    if c in ');(' or (c == '}' and db == 0) or (c == '{' and db == 1):
        print(line, c, 'p=', dp, 'b=', db)
