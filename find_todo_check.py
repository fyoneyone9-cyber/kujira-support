import re
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if any(k in l for k in ['todo', 'Todo', 'TODO', 'check', 'Check', '次にすべき', 'memo', 'Memo', 'textarea', 'saveMemo', 'dashboard_memo']):
        print(f'{i}: {l}', end='')
