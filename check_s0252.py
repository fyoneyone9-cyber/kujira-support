# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    c = f.read()

# S0252定義を探す
m = re.search(r"['\"]S0252['\"].*?:\s*\[", c)
if m:
    start = m.start()
    print('Found at pos:', start)
    print(c[start:start+3000])
else:
    # OUTFIT_REF定義を探す
    m2 = re.search(r"OUTFIT_REFS.*?S0252", c[:100000], re.DOTALL)
    if m2:
        print('In OUTFIT_REFS')
    # 別パターン
    hits = [i for i in range(len(c)) if c[i:i+5] == 'S0252']
    print(f'S0252 occurrences: {len(hits)}')
    for h in hits[:3]:
        print(c[h-50:h+200])
        print('---')
