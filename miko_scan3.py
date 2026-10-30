# -*- coding: utf-8 -*-
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\AI\ComfyUI\dashboard.html'
s = open(p, encoding='utf-8').read()
i = s.find('char_miko_s1_youjo_a')
print('first occurrence at', i)
print(repr(s[i-120:i+600]))
# count occurrences
print('count:', s.count('char_miko_s1_youjo_a'))
