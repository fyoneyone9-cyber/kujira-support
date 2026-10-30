import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if any(k in l for k in ['worker_needed', '作業員', 'WorkerSection', 'worker_contacts', '手配必要']):
        print(f'{i}: {l}', end='')
