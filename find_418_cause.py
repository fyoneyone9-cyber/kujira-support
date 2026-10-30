import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, encoding='utf-8') as f:
    lines = f.readlines()

# React #418 = hydration mismatch due to text differences server vs client
# Common causes:
# 1. {new Date()} in render
# 2. Math.random() in render
# 3. typeof window checks
# 4. Conditional rendering based on client-only state

issues = []
for i, l in enumerate(lines, 1):
    s = l.strip()
    if 'new Date()' in s and 'use' not in s.lower():
        issues.append(f'L{i} new Date(): {s[:100]}')
    if 'Math.random' in s:
        issues.append(f'L{i} Math.random: {s[:100]}')
    if 'typeof window' in s:
        issues.append(f'L{i} typeof window: {s[:100]}')
    if 'localStorage' in s:
        issues.append(f'L{i} localStorage: {s[:100]}')
    if 'navigator' in s and 'rel=' not in s:
        issues.append(f'L{i} navigator: {s[:100]}')

print('\n'.join(issues[:40]))
