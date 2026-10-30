# -*- coding: utf-8 -*-
# char_onsen_ol_A の出現位置と周辺構造を確認（複数出現・配列形式の可能性）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
for m in re.finditer(r"id[\"']?\s*:\s*[\"']char_onsen_ol_A[\"']", s):
    i = m.start()
    print('POS', i, 'line', s[:i].count('\n')+1)
    print(repr(s[max(0,i-300):i+150]))
    print('---')
