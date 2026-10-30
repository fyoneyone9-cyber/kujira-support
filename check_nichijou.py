# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    c = f.read()

# kaizo_nichijou系キャラを全部探す
hits = re.findall(r"id:['\"]char_kaizo_nichijou[^'\"]*['\"]", c)
print(f'Total kaizo_nichijou chars: {len(hits)}')
# S別に集計
for h in sorted(set(hits)):
    print(' ', h[:80])
