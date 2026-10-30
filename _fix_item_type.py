# -*- coding: utf-8 -*-
"""型名が Item ではなく DeliveryItem だったので修正。"""
import io
p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
s = io.open(p, encoding="utf-8").read()
old = "  const siblingsOf = (it: Item) =>"
assert s.count(old) == 1, "anchor"
s = s.replace(old, "  const siblingsOf = (it: DeliveryItem) =>", 1)
io.open(p, "w", encoding="utf-8").write(s)
print("fixed")
