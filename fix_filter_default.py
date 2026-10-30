# -*- coding: utf-8 -*-
path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

old = "const [assigneeFilter, setAssigneeFilter] = useState<string>('all')"
new = "const [assigneeFilter, setAssigneeFilter] = useState<string>('\u7c73\u5c71')"

if old in content:
    content = content.replace(old, new, 1)
    print('OK: default -> 米山')
else:
    print('ERROR: not found')
    import re
    m = re.search(r"assigneeFilter.*useState", content)
    if m:
        print('Found at:', repr(content[m.start():m.start()+80]))

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done')
