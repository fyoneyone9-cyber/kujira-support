# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 末尾から "  )\n}\n" を探して {AlertPopup} を挿入
# ファイルの最後3行を確認して挿入
total = len(lines)
# 末尾: ...  )\n}\n  → 末尾2行が '  )\n' と '}\n'
for i in range(total-1, total-10, -1):
    if lines[i].rstrip() == '}' and lines[i-1].rstrip() == '  )':
        # lines[i-1] の前に {AlertPopup} を挿入
        lines.insert(i-1, '    {AlertPopup}\n')
        print(f'Inserted at line {i-1+1}')
        break

with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done')
