# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\quality_rules\real.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('Keys:', list(d.keys()))

# pos_drop を確認
pos_drop = d.get('pos_drop', [])
print(f'\npos_drop ({len(pos_drop)} items):')
for x in pos_drop:
    if 'collar' in x or 'leash' in x or 'fours' in x or 'slave' in x or 'submiss' in x:
        print(f'  HIT: {x}')

# conflicts を確認
conflicts = d.get('conflicts', [])
print(f'\nconflicts ({len(conflicts)} groups):')
for g in conflicts:
    items = str(g)
    if 'collar' in items or 'leash' in items or 'fours' in items or 'slave' in items:
        print(f'  HIT: {items[:200]}')
