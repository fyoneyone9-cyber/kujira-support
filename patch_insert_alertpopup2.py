# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# {AlertPopup} を除去して正しい位置に再挿入
c = c.replace('    {AlertPopup}\n  )\n}', '  )\n}')

# return ( の直後の <div をフラグメントで包む
# "  return (\n    <div" → "  return (\n    <>\n    <div"
# 末尾の "    </div>\n  )" → "    </div>\n    {AlertPopup}\n    </>\n  )"

# return文の最外divを特定: "  return (\n    <div className=\"min-h-screen"
c = c.replace(
    'return (\n    <div className="min-h-screen',
    'return (\n    <>\n    <div className="min-h-screen'
)

# 末尾の </div>\n  ) を </div>\n    {AlertPopup}\n    </>\n  ) に
c = c.replace(
    '    </div>\n  )\n}',
    '    </div>\n    {AlertPopup}\n    </>\n  )\n}'
)

with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done')
