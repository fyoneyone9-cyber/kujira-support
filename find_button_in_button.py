import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', encoding='utf-8') as f:
    lines = f.readlines()

# buttonタグの開閉を追跡してネストを検出
depth = 0
for i, l in enumerate(lines, 1):
    stripped = l.strip()
    opens = stripped.count('<button') - stripped.count('</button') - stripped.count('/>')
    if depth > 0 and '<button' in stripped and '</button' not in stripped:
        print(f'NESTED BUTTON at line {i} (depth={depth}): {stripped[:100]}')
    depth = max(0, depth + opens)
    if depth > 0:
        pass  # inside button
