import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

markers = [
    ('切り返しナビ', '切り返しナビ'),
    ('AI切り返し', 'AI切り返し'),
    ('米山パターン', '米山パターン'),
    ('キーワードで', 'キーワード検索'),
    ('activeTab === \'script\'', 'script tab start'),
]

for i, l in enumerate(lines):
    for key, label in markers:
        if key in l:
            print(f"L{i+1} [{label}]: {l.strip()[:70]}")
            break
