import re

path = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
with open(path, encoding='utf-8') as f:
    content = f.read()

# 1) 入金ステータスに「見積書送付済み」を追加
old_pay = "['入金不要（無償）', '請求未発行', '請求書発行済', '入金待ち', '入金確認済み', '入金超過・要確認']"
new_pay = "['入金不要（無償）', '請求未発行', '見積書送付済み', '請求書発行済', '入金待ち', '入金確認済み', '入金超過・要確認']"
if old_pay in content:
    content = content.replace(old_pay, new_pay)
    print("✅ 入金ステータス修正OK")
else:
    print("❌ 入金ステータスのパターンが見つかりません")

# 2) badgeColor に見積書送付済みの色を追加
old_badge = "payStatus === '請求書発行済' ? 'bg-blue-800 text-blue-200' :"
new_badge = "payStatus === '見積書送付済み' ? 'bg-teal-800 text-teal-200' :\n    payStatus === '請求書発行済' ? 'bg-blue-800 text-blue-200' :"
if old_badge in content:
    content = content.replace(old_badge, new_badge)
    print("✅ badgeColor修正OK")
else:
    print("❌ badgeColorのパターンが見つかりません")

# 3) 作業員手配チェックボックスを worker_estimate_status と同期
# isJit判定の直後に isWorker 判定を追加
old_cb = """                      const isJit = label.startsWith('JITボックス')
                      const jitDone = isJit && it.jitbox_ordered !== null && it.jitbox_ordered !== undefined
                      const checked = jitDone || !!(it.dashboard_todos?.[label] as boolean)"""

new_cb = """                      const isJit = label.startsWith('JITボックス')
                      const jitDone = isJit && it.jitbox_ordered !== null && it.jitbox_ordered !== undefined
                      const isWorker = label === '作業員 手配'
                      const workerDone = isWorker && (it.dashboard_todos?.['worker_estimate_status'] as string) === '作業完了'
                      const checked = jitDone || workerDone || !!(it.dashboard_todos?.[label] as boolean)"""

if old_cb in content:
    content = content.replace(old_cb, new_cb)
    print("✅ 作業員チェック同期OK")
else:
    print("❌ チェックボックスのパターンが見つかりません")

# 4) チェックボックスのdisabledとonChangeにworkerDoneも追加
old_dis = "disabled={jitDone}"
new_dis = "disabled={jitDone || workerDone}"
if old_dis in content:
    content = content.replace(old_dis, new_dis)
    print("✅ disabled修正OK")
else:
    print("❌ disabledのパターンが見つかりません")

old_onchange = "onChange={() => { if (!jitDone) saveTodoKey(it.id, it.dashboard_todos, label, checked ? '' : '1') }}"
new_onchange = "onChange={() => { if (!jitDone && !workerDone) saveTodoKey(it.id, it.dashboard_todos, label, checked ? '' : '1') }}"
if old_onchange in content:
    content = content.replace(old_onchange, new_onchange)
    print("✅ onChange修正OK")
else:
    print("❌ onChangeのパターンが見つかりません")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("\n完了")
