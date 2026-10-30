import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
with open(path, encoding='utf-8') as f:
    content = f.read()

old = "            const ltWarnings: string[] = []"
new = """            const ltWarnings: string[] = []
            if (!it.slack_url) ltWarnings.push('SlackリンクがURLセクションに未登録')
            if (!it.process_sheet_url) ltWarnings.push('工程表リンクが未登録')
            if (!it.hearing_sheet_url) ltWarnings.push('ヒアリングシートリンクが未登録')"""

if old in content:
    content = content.replace(old, new)
    print("OK")
else:
    print("NOT FOUND")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
