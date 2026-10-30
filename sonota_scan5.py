# -*- coding: utf-8 -*-
# ラベルが見つからない原因調査: 生出現数と、unicodeエスケープ格納の可能性を確認
import re, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
for t in ['ルシア', '捕食ミア', 'エンタコール', '無乳 幼女', '触手幼女']:
    print(t, 'raw count:', s.count(t))
    esc = t.encode('unicode_escape').decode().replace('\\x', '\\u00')
    u = ''.join('\\u%04x' % ord(c) for c in t)
    print(t, 'escaped count:', s.count(u))
