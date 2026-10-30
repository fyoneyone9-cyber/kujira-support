# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 156行目付近に誤挿入されたprogressAlertCountブロックを削除
new_lines = []
skip = 0
for i, line in enumerate(lines):
    if skip > 0:
        skip -= 1
        continue
    # 誤挿入ブロックを検出（156行目付近・コンポーネント外）
    if i < 200 and line.strip() == 'const progressAlertCount = allItems.filter(i => {':
        # 7行スキップ（定義+空行）
        skip = 7
        continue
    new_lines.append(line)

# 正しい位置（return直前）に挿入
# useState の後ろ、return (  の直前（500行以降）
result = []
inserted = False
for i, line in enumerate(new_lines):
    if not inserted and i > 400 and line.strip() == 'return (':
        result.append('  const progressAlertCount = allItems.filter(i => {\n')
        result.append('    if (i.status === \'done\') return false\n')
        result.append('    const due = new Date(i.delivery_due_date)\n')
        result.append('    const diff = (due.getTime() - Date.now()) / (1000 * 60 * 60 * 24)\n')
        result.append('    return diff <= 14\n')
        result.append('  }).length\n')
        result.append('\n')
        inserted = True
    result.append(line)

with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'w', encoding='utf-8') as f:
    f.writelines(result)
print('Done, inserted at line', next(i for i, l in enumerate(result) if 'const progressAlertCount' in l))
