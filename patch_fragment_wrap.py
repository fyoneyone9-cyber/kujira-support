# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 531行目: "  return (\n" → "  return (\n    <>\n"
# 1021行目（末尾）の前: "    {AlertPopup}\n  )\n}" → "    {AlertPopup}\n    </>\n  )\n}"

total = len(lines)

# 531行目（0-indexed: 530）の次の行の前に <> を追加
# lines[530] = "  return (\n"
# lines[531] = "    <div>\n"  ← ここの前に <> を入れる
lines.insert(531, '    <>\n')
print('Inserted <> at line 532')

# 末尾を修正: {AlertPopup} の後に </> を追加
# 現在: ...{AlertPopup}\n  )\n}
# ファイル末尾から {AlertPopup} を探す
for i in range(len(lines)-1, len(lines)-10, -1):
    if '{AlertPopup}' in lines[i]:
        lines.insert(i+1, '    </>\n')
        print(f'Inserted </> at line {i+2}')
        break

with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'w', encoding='utf-8') as f:
    f.writelines(lines)
print('Done')
