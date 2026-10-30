import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines, 1):
    if 'getElementById' in l and 'worker' in l:
        print(f'{i}: {repr(l)}')
