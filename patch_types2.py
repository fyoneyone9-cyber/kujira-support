# -*- coding: utf-8 -*-
path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = '  equipment_arrival_dates?: Record<string, string> | null\n}'
new = '  equipment_arrival_dates?: Record<string, string> | null\n  locked?: boolean | null\n  jitbox_ordered?: boolean | null\n}'

if old in content:
    content = content.replace(old, new, 1)
    print('Type fields added OK')
else:
    print('ERROR: type not found')
    # debug
    idx = content.find('equipment_arrival_dates')
    print(repr(content[idx:idx+60]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done.')
