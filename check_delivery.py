# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    c = f.read()
print("type OK" if "'alert' | 'all' | 'progress' | 'done'" in c else "TYPE MISSING")
print("progress filter OK" if "filter === 'progress'" in c else "PROGRESS FILTER MISSING")
print("button OK" if '\u9032\u884c\u4e2d' in c else "BUTTON MISSING")

# 型エラーになりそうな箇所チェック
import re
# useState type
m = re.search(r"useState<([^>]+)>\('alert'\)", c)
if m:
    print("useState type:", m.group(1))
