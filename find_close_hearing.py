import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if 'hearing_nav_skip' in l or 'ナビゲート不要' in l or 'Geminiプロンプト' in l:
        print(f'{i}: {l}', end='')
