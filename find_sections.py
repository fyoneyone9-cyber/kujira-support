with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    s = l.strip()
    markers = ['script &&', 'AI', 'hubspot &&', 'status &&', 'knowledge &&']
    for m in markers:
        if m in s and len(s) < 60:
            print(i+1, repr(s[:60]))
            break
