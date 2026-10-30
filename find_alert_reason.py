import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, encoding='utf-8') as f:
    lines = f.readlines()

# getAlertReasonの定義を探す
in_func = False
for i, l in enumerate(lines, 1):
    if 'getAlertReason' in l or 'ltWarnings' in l:
        if i not in [813]: # skip known
            print(f'{i}: {l}', end='')
