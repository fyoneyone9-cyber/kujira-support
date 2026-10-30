# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    c = f.read()

# OUTFIT_REFS or window.OUTFIT_REFS でS0252を定義しているブロック
m = re.search(r"(window\.OUTFIT_REFS\s*=\s*window\.OUTFIT_REFS.*?)\n\n", c, re.DOTALL)
if m:
    print(m.group()[:500])

# S0252キーを持つオブジェクト
m2 = re.search(r"['\"]S0252['\"]\s*:\s*\[(\{.*?\})\]", c, re.DOTALL)
if m2:
    print('Found array:')
    labels = re.findall(r"label:'([^']+)'", m2.group())
    for i,l in enumerate(labels):
        print(f'  {i+1:02d}: {l}')

# 全OUTFIT_REFS定義位置
for m3 in re.finditer(r"OUTFIT_REFS", c):
    print(f'pos={m3.start()}: {c[m3.start():m3.start()+100]}')
    break
