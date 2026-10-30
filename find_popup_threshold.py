import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if any(k in l for k in ['popupAlert', 'POPUP', '10日', '21日', 'daysLeft', 'days <=', 'days<', '<= 10', '<= 21', 'threshold']):
        print(f'{i}: {l}', end='')
