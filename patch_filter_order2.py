# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# "progressAlertCount" が既に存在するか確認
content = ''.join(lines)
if 'progressAlertCount' in content and 'const progressAlertCount' not in content:
    # 変数定義が挿入されていない。return直前の行を探して挿入
    new_lines = []
    inserted = False
    for i, line in enumerate(lines):
        if not inserted and line.strip().startswith('return (') and i > 100:
            new_lines.append('  const progressAlertCount = allItems.filter(i => {\n')
            new_lines.append('    if (i.status === \'done\') return false\n')
            new_lines.append('    const due = new Date(i.delivery_due_date)\n')
            new_lines.append('    const diff = (due.getTime() - Date.now()) / (1000 * 60 * 60 * 24)\n')
            new_lines.append('    return diff <= 14\n')
            new_lines.append('  }).length\n')
            new_lines.append('\n')
            inserted = True
        new_lines.append(line)
    with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print('Inserted progressAlertCount before return')
else:
    print('Already OK or not needed')
