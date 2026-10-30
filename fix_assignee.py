# -*- coding: utf-8 -*-
path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 文字化けした assigneeFilter の初期値を 'all' に修正
# (後でUIから担当者フィルタが選べるので 'all' がデフォルトで安全)
import re
fixed, n = re.subn(
    r"useState<string>\('[^']*'\)(\s*//.*)?(\s*// assignee)",
    "useState<string>('all')",
    content
)
if n == 0:
    # パターン2: 文字化け行を直接置換
    lines = content.split('\n')
    new_lines = []
    changed = False
    for line in lines:
        if 'assigneeFilter, setAssigneeFilter' in line and 'useState' in line:
            new_lines.append("  const [assigneeFilter, setAssigneeFilter] = useState<string>('all')")
            changed = True
            print(f'Fixed: {repr(line.strip())}')
        else:
            new_lines.append(line)
    if changed:
        fixed = '\n'.join(new_lines)
        n = 1
    else:
        fixed = content

if n > 0:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(fixed)
    print('Done. assigneeFilter default -> all')
else:
    print('ERROR: pattern not found')
