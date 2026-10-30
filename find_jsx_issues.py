import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, encoding='utf-8') as f:
    lines = f.readlines()

# 閉じタグ問題を探す: </div>} パターン（正常）vs </div>}{/* */} など
for i, l in enumerate(lines, 1):
    s = l.strip()
    # {openSections && <div>} の閉じが </div>} になってるか確認
    if re.search(r'</div>\s*\}\s*\{?/\*', s):
        print(f'L{i} closing: {s[:120]}')
    if re.search(r'openSections\[', s):
        print(f'L{i} openSections: {s[:120]}')
