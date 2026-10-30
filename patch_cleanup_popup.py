# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# 全ての誤挿入を除去
c = c.replace('    {AlertPopup}\n    </>\n  )\n}', '  )\n}')
c = c.replace('    {AlertPopup}\n  )\n}', '  )\n}')
c = c.replace('    {AlertPopup}\n', '')
c = c.replace('    </>\n  )\n}', '  )\n}')
c = c.replace('return (\n    <>\n    <div', 'return (\n    <div')

# 末尾を確認して正しい位置に挿入
# メインコンポーネントの末尾は "    </div>\n  )\n}" で終わるはず
# 最後の "    </div>\n  )\n}" に {AlertPopup} を挿入
# → "    </div>\n    {AlertPopup}\n  )\n}"
# ただし最後の1箇所だけ

# 末尾から最後の "    </div>\n  )\n}" を探す
target = '    </div>\n  )\n}'
last_pos = c.rfind(target)
if last_pos != -1:
    # その前後を確認
    context = c[last_pos-50:last_pos+len(target)+10]
    print('Found at:', last_pos, 'context:', repr(context[:80]))
    # ここに {AlertPopup} を挟む
    new_ending = '    </div>\n    {AlertPopup}\n  )\n}'
    c = c[:last_pos] + new_ending + c[last_pos+len(target):]
    print('Inserted AlertPopup at position', last_pos)
else:
    print('Target not found! Tail:')
    print(repr(c[-200:]))

with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
