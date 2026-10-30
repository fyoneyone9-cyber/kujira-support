import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if any(k in l for k in ['markDone', 'zoom_url', 'Zoom', 'spread_url', 'spreadsheet', '管理スプレッド', 'process_sheet']):
        print(f'{i}: {l}', end='')
