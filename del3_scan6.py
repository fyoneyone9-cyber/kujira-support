# -*- coding: utf-8 -*-
# lolihypapp/jitsufu GD定義の実フォーマットを確認
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
i = s.find("key:'lolihypapp_s1'")
print(repr(s[max(0,i-50):i+250]))
print('===')
j = s.find("key:'jitsufu_s1'")
print(repr(s[max(0,j-50):j+250]))
