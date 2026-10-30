# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    c = f.read()

# S3のキャラ一覧
s3 = re.findall(r"id:['\"]char_kaizo_nichijou3_([^'\"]+)['\"]", c)
print(f'S3 chars: {s3}')

# S3 tifaの完全なpush()ブロックを取得
m = re.search(r"(window\.CHAR_TEMPLATES\.female\.push\(\{[^}]*?id:['\"]char_kaizo_nichijou3_tifa['\"].*?\}\);)", c, re.DOTALL)
if m:
    print('\nS3 tifa block:')
    print(m.group()[:2000])
