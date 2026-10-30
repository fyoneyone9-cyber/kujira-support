import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', encoding='utf-8') as f:
    lines = f.readlines()
# チェックボックスUIと自由記入欄を探す
for i, l in enumerate(lines, 1):
    if any(k in l for k in ['checkbox', 'Checkbox', 'saveMemo', 'dashboard_memo', 'textarea', '自由', 'メモ', 'フリー', '次にすべき', 'todoItems', 'TodoItem']):
        print(f'{i}: {l}', end='')
