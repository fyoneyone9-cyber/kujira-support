# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# arriveVsDue の後、<div の前に return ( を挿入
old = '  const arriveVsDue = expectedArrive && dueDate ? daysLeft(dueDate) - daysLeft(expectedArrive) : null\n\n    <div'
new = '  const arriveVsDue = expectedArrive && dueDate ? daysLeft(dueDate) - daysLeft(expectedArrive) : null\n\n  return (\n    <div'

if old in content:
    content = content.replace(old, new)
    print('Fixed return (')
else:
    print('Pattern not found, trying alternate...')
    old2 = '  const arriveVsDue = expectedArrive && dueDate ? daysLeft(dueDate) - daysLeft(expectedArrive) : null\n\n    <div'
    print(repr(content[content.find('arriveVsDue'):content.find('arriveVsDue')+200]))

with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'w', encoding='utf-8') as f:
    f.write(content)
