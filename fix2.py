import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
with open(path, encoding='utf-8') as f:
    content = f.read()

results = []

# 1) 入金ステータスリストに「見積書送付済み」を追加
old1 = "['入金不要（無償）', '請求未発行', '請求書発行済', '入金待ち', '入金確認済み', '入金超過・要確認']"
new1 = "['入金不要（無償）', '請求未発行', '見積書送付済み', '請求書発行済', '入金待ち', '入金確認済み', '入金超過・要確認']"
if old1 in content:
    content = content.replace(old1, new1)
    results.append("pay_status: OK")
else:
    results.append("pay_status: NOT FOUND")

# 2) badgeColor に見積書送付済みの色追加
old2 = "payStatus === '請求書発行済' ? 'bg-blue-800 text-blue-200' :"
new2 = "payStatus === '見積書送付済み' ? 'bg-teal-800 text-teal-200' :\n    payStatus === '請求書発行済' ? 'bg-blue-800 text-blue-200' :"
if old2 in content:
    content = content.replace(old2, new2)
    results.append("badge: OK")
else:
    results.append("badge: NOT FOUND")

# 3) チェックボックスに workerDone 同期を追加
# まず現在の該当箇所を探す
marker = "const isJit = label.startsWith('JITボックス')"
idx = content.find(marker)
if idx >= 0:
    # 該当箇所のブロックを特定して置換
    old3 = (
        "const isJit = label.startsWith('JITボックス')\n"
        "                      const jitDone = isJit && it.jitbox_ordered !== null && it.jitbox_ordered !== undefined\n"
        "                      const checked = jitDone || !!(it.dashboard_todos?.[label] as boolean)"
    )
    new3 = (
        "const isJit = label.startsWith('JITボックス')\n"
        "                      const jitDone = isJit && it.jitbox_ordered !== null && it.jitbox_ordered !== undefined\n"
        "                      const isWorker = label === '作業員 手配'\n"
        "                      const workerDone = isWorker && (it.dashboard_todos?.['worker_estimate_status'] as string) === '作業完了'\n"
        "                      const checked = jitDone || workerDone || !!(it.dashboard_todos?.[label] as boolean)"
    )
    if old3 in content:
        content = content.replace(old3, new3)
        results.append("worker_sync: OK")
    else:
        # スペース数が違う可能性があるので段階的に確認
        results.append("worker_sync: pattern mismatch - checking...")
        snippet = content[idx:idx+400]
        results.append(f"  found: {repr(snippet[:200])}")
else:
    results.append("worker_sync: marker not found")

# 4) disabled
if "disabled={jitDone}" in content:
    content = content.replace("disabled={jitDone}", "disabled={jitDone || workerDone}")
    results.append("disabled: OK")
else:
    results.append("disabled: NOT FOUND")

# 5) onChange
old5 = "onChange={() => { if (!jitDone) saveTodoKey(it.id, it.dashboard_todos, label, checked ? '' : '1') }}"
new5 = "onChange={() => { if (!jitDone && !workerDone) saveTodoKey(it.id, it.dashboard_todos, label, checked ? '' : '1') }}"
if old5 in content:
    content = content.replace(old5, new5)
    results.append("onChange: OK")
else:
    results.append("onChange: NOT FOUND")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

for r in results:
    print(r)
