# -*- coding: utf-8 -*-
# manga_mahou / tentacle_nurse 等のid定義の実フォーマットを特定（複数行push・スペース有無対応）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
# id: の後にスペースや改行があるケースも拾う
ids = sorted(set(re.findall(r"id:\s*[\"'](char_manga_mahou_[a-zA-Z0-9_]*)[\"']", s)))
print('manga_mahou ids (loose):', len(ids))
# それでも0なら生の出現箇所を見る
for m in list(re.finditer(r'char_manga_mahou_[a-zA-Z0-9_]*', s))[:6]:
    i = m.start()
    print(m.group(0), '||', repr(s[max(0,i-60):i+40])[:140])
    print('---')
print('=== tentacle_nurse ===')
for m in list(re.finditer(r'char_tentacle_nurse_[a-zA-Z0-9_]*', s))[:4]:
    i = m.start()
    print(m.group(0), '||', repr(s[max(0,i-60):i+40])[:140])
    print('---')
print('=== magic_youjo ===')
for m in list(re.finditer(r'char_magic_youjo_?[a-zA-Z0-9_]*', s))[:4]:
    i = m.start()
    print(m.group(0), '||', repr(s[max(0,i-60):i+40])[:140])
    print('---')
