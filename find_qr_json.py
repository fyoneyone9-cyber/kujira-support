# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding='utf-8')

# _DIR を確認
with open(r'C:\AI\ComfyUI\quality_rules.py', 'r', encoding='utf-8') as f:
    for i, l in enumerate(f):
        if '_DIR' in l and ('os.path' in l or '__file__' in l):
            print(f'L{i+1}: {l.rstrip()}')

# quality_rules フォルダを探す
for root, dirs, files in os.walk(r'C:\AI\ComfyUI'):
    if 'quality_rules' in dirs:
        qr_path = os.path.join(root, 'quality_rules')
        print(f'\nFound: {qr_path}')
        for f in os.listdir(qr_path):
            print(f'  {f}')
        break
