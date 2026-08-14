import sys
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\teleapo\page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

targets = ["activeTab === 'script'", "activeTab === 'hubspot'", "activeTab === 'status'",
           "activeTab === 'knowledge'", "AI\u5207\u308a\u8fd4\u3057", "\u5207\u308a\u8fd4\u3057\u30ca\u30d3",
           "\u7c73\u5c71\u30d1\u30bf\u30fc\u30f3", "\u30ad\u30fc\u30ef\u30fc\u30c9\u3067"]
for i, l in enumerate(lines):
    for t in targets:
        if t in l:
            print(i+1, l.strip()[:70])
            break
