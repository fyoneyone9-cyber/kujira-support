import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

import re
# ロヒプノール系のchar_id一覧
matches = re.findall(r"id:\s*'(char_rohypnol[^']*)'", content)
for m in sorted(set(matches)):
    print(m)

print('---')
# S1の最初のキャラの構造を確認
m = re.search(r"(window\.CHAR_TEMPLATES\.female\.push\(\{[^}]*id:\s*'char_rohypnol[^']*'.*?\}\);)", content, re.DOTALL)
if m:
    print(m.group(1)[:800])
