import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if '入金管理' in l:
        print(f'{i}: {l}', end='')
        # 前後5行も表示
        for j in range(max(0,i-6), i-1):
            print(f'  {j+1}: {lines[j]}', end='')
