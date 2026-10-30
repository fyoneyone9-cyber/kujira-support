# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\quality_rules\real.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

groups = d.get('dedupe_groups', [])
print(f'dedupe_groups: {len(groups)} groups')
for g in groups:
    name = g.get('name','')
    items = json.dumps(g, ensure_ascii=False)
    if 'collar' in items or 'leash' in items or 'people' in name or 'count' in name or 'solo' in name or 'person' in name:
        print(f'\nGROUP: {name}')
        print(json.dumps(g, ensure_ascii=False, indent=2)[:500])
