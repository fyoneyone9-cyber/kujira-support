import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
with open(path, encoding='utf-8') as f:
    content = f.read()

# ステータスリストに追加（請求未発行の直後）
old1 = "['入金不要（無償）', '請求未発行', '見積書送付済み', '請求書発行済', '入金待ち', '入金確認済み', '入金超過・要確認']"
new1 = "['入金不要（無償）', '請求未発行', '見積書作成中（確認中）', '見積書送付済み', '請求書発行済', '入金待ち', '入金確認済み', '入金超過・要確認']"
if old1 in content:
    content = content.replace(old1, new1)
    print("list: OK")
else:
    print("list: NOT FOUND")

# badgeColorに色追加（見積書送付済みの直前）
old2 = "payStatus === '見積書送付済み' ? 'bg-teal-800 text-teal-200' :"
new2 = "payStatus === '見積書作成中（確認中）' ? 'bg-indigo-800 text-indigo-200' :\n    payStatus === '見積書送付済み' ? 'bg-teal-800 text-teal-200' :"
if old2 in content:
    content = content.replace(old2, new2)
    print("badge: OK")
else:
    print("badge: NOT FOUND")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("完了")
