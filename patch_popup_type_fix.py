# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# alerts 配列の型アノテーションを修正
c = c.replace(
    "    const alerts: {client: string; reason: string; days: number}[] = []",
    "    const alerts: {id: string; client: string; reason: string; days: number; assignee: string}[] = []"
)

with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done')
