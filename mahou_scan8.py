# -*- coding: utf-8 -*-
# manga_mahou キャラの定義コンテキストを確認（idキー形式を特定）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
for name in ['char_manga_mahou_jc_aoi', 'char_manga_mahou_jk_akane', 'char_manga_mahou_jk_yuri_tentacle']:
    for m in re.finditer(re.escape(name), s):
        i = m.start()
        print(name, '||', repr(s[max(0,i-100):i+60])[:200])
        print('---')
