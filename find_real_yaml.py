# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
# quality_rules の設定ファイル(yaml/json)を探す
for root, dirs, files in os.walk(r'C:\AI\ComfyUI'):
    for f in files:
        if 'quality' in f.lower() and (f.endswith('.yaml') or f.endswith('.yml') or f.endswith('.json')):
            print(os.path.join(root, f))
        if f == '_common.yaml' or f == 'real.yaml' or f == 'krea2.yaml':
            print(os.path.join(root, f))
