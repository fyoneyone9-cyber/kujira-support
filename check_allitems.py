# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# allItems state確認
print("allItems state:", "useState<DeliveryItem[]>([])" in c and "allItems" in c)
# setAllItems確認
print("setAllItems called:", "setAllItems(all)" in c)
# useEffect でloadStats呼ばれてるか
import re
effects = re.findall(r'useEffect\([^)]+\)', c)
print("useEffect count:", len(re.findall(r'useEffect\(', c)))
# loadStats の呼び出し箇所
for i, line in enumerate(c.split('\n')):
    if 'loadStats' in line:
        print(f"L{i+1}: {line.strip()}")
