path = r'C:\Users\fyone\Desktop\kujira-support\src\app\(app)\dashboard\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Two columnsブロック（最近のログ・マニュアル）を丸ごと削除
import re
c = re.sub(r'\s*\{/\* Two columns \*/\}.*', '', c, flags=re.DOTALL)
# 末尾に閉じタグを補完
c = c.rstrip() + '\n    </div>\n  )\n}\n'

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
print('done')
