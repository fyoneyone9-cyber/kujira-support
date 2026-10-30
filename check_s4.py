# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    c = f.read()

# S4キャラを探す
s4 = re.findall(r"id:['\"]char_kaizo_nichijou4_[^'\"]*['\"]", c)
print(f'S4 chars found: {len(s4)}')
for x in s4:
    print(' ', x[:80])

# S3のoutfits数確認（比較用）
s3_sample = re.search(r"id:['\"]char_kaizo_nichijou3_tifa['\"].*?outfits:\s*\[.*?\]", c, re.DOTALL)
if s3_sample:
    outfits = re.findall(r"label:['\"]([^'\"]+)['\"]", s3_sample.group()[:3000])
    print(f'\nS3 tifa outfits ({len(outfits)}):')
    for o in outfits:
        print(' ', o)
