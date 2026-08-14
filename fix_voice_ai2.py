import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

# 現在の状態確認
lines = content.split('\n')
for i, l in enumerate(lines[525:545], 526):
    print(i, l[:80])
