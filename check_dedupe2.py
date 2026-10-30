# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\quality_rules\real.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

groups = d.get('dedupe_groups', [])
print('All group names:')
for g in groups:
    print(f'  {g.get("name")}: any={g.get("any",[])[:5]}')
