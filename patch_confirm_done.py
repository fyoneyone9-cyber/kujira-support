# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# markDone に confirm を追加
old = "  const markDone = (id: string) => patch(id, { status: 'done', acknowledged_at: new Date().toISOString() })"
new = (
    "  const markDone = (id: string) => {\n"
    "    if (!window.confirm('\u672c\u5f53\u306b\u7d0d\u54c1\u5b8c\u4e86\u3057\u307e\u3057\u305f\u304b\uff1f\\n\\n\u300c\u306f\u3044\u300d\u3092\u62bc\u3059\u3068\u300c\u7d0d\u54c1\u5b8c\u4e86\u5206\u300d\u306b\u79fb\u52d5\u3057\u307e\u3059\u3002')) return\n"
    "    patch(id, { status: 'done', acknowledged_at: new Date().toISOString() })\n"
    "  }"
)
c = c.replace(old, new)

with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done')
