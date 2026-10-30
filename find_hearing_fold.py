import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if 'hearing_open' in l or '_hearing_open_' in l or 'hOpen' in l or 'document.getElementById' in l:
        print(f'{i}: {repr(l)}')
