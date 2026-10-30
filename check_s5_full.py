# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    lines = f.readlines()

l = lines[432259]  # S5 jk_A行
# outfits部分を抽出
m = re.search(r"outfits:\[.*", l)
if m:
    outfits_str = m.group()
    # label を全部抽出
    labels = re.findall(r"label:'([^']+)'", outfits_str)
    prompts = re.findall(r"prompt:'([^']+)'", outfits_str)
    print(f'S5 jk_A outfits count: {len(labels)}')
    for i, (lb, pr) in enumerate(zip(labels, prompts)):
        print(f'  {i:02d}: {lb}')
        print(f'      prompt: {pr[:80]}')
