# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 156行目付近: arriveVsDue の後に return ( が欠けている
# "  const arriveVsDue = ..." の次の行が <div になっている → return ( を挿入
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if 'const arriveVsDue = expectedArrive' in line:
        # 次の行が return ( でなければ追加
        next_line = lines[i+1].strip() if i+1 < len(lines) else ''
        if next_line.startswith('<div'):
            new_lines.append('  return (\n')
            print(f'Inserted return ( after line {i+1}')

with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
print('Done')
