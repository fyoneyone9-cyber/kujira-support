import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\GensparkClaw\kujira-support\src\components\Sidebar.tsx', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if any(k in l for k in ['nippou', '勤怠', 'WorkTimer', 'href', 'navItems', 'icon']):
        print(f'{i}: {l}', end='')
