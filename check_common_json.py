# -*- coding: utf-8 -*-
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\quality_rules\_common.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

print('Keys:', list(d.keys()))

for section in ['pos_drop', 'pos_cap_immune', 'conflicts']:
    items = d.get(section, [])
    print(f'\n{section} ({len(items)} items):')
    for x in items:
        s = str(x)
        if 'collar' in s or 'leash' in s or 'fours' in s or 'slave' in s or 'submiss' in s or 'chain' in s:
            print(f'  HIT: {s[:200]}')
