import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, encoding='utf-8') as f:
    content = f.read()

# ファイル先頭に dynamic export を追加（既にある場合はスキップ）
if "export const dynamic = 'force-dynamic'" not in content:
    # 'use client'の直後に追加
    content = content.replace(
        "'use client'\n",
        "'use client'\n\nexport const dynamic = 'force-dynamic'\n",
        1
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Added force-dynamic export')
else:
    print('Already has force-dynamic')
