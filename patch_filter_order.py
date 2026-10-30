# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. ボタン順番を並べ替え: 未納品のみ → 納品管理（進行中） → 納品完了分 → 全件表示
old_buttons = (
    '        <button onClick={() => setFilter(\'alert\')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === \'alert\' ? \'bg-red-600 text-white\' : \'bg-slate-700 text-slate-300 hover:bg-slate-600\'}`}>\u672a\u7d0d\u54c1\u306e\u307f</button>\n'
    '        <button onClick={() => setFilter(\'all\')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === \'all\' ? \'bg-blue-600 text-white\' : \'bg-slate-700 text-slate-300 hover:bg-slate-600\'}`}>\u5168\u4ef6\u8868\u793a</button>\n'
    '        <button onClick={() => setFilter(\'progress\')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === \'progress\' ? \'bg-yellow-600 text-white\' : \'bg-slate-700 text-slate-300 hover:bg-slate-600\'}`}>\u7d0d\u54c1\u7ba1\u7406\uff08\u9032\u884c\u4e2d\uff09</button>\n'
    '        <button onClick={() => setFilter(\'done\')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === \'done\' ? \'bg-green-600 text-white\' : \'bg-slate-700 text-slate-300 hover:bg-slate-600\'}`}>\u7d0d\u54c1\u5b8c\u4e86\u5206</button>'
)

# 進行中ボタンに14日以内アラーム件数バッジを追加
new_buttons = (
    '        <button onClick={() => setFilter(\'alert\')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === \'alert\' ? \'bg-red-600 text-white\' : \'bg-slate-700 text-slate-300 hover:bg-slate-600\'}`}>\u672a\u7d0d\u54c1\u306e\u307f</button>\n'
    '        <button onClick={() => setFilter(\'progress\')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === \'progress\' ? \'bg-yellow-600 text-white\' : \'bg-slate-700 text-slate-300 hover:bg-slate-600\'}`}>\u7d0d\u54c1\u7ba1\u7406\uff08\u9032\u884c\u4e2d\uff09{progressAlertCount > 0 && <span className="ml-1 bg-red-500 text-white text-xs rounded-full px-1.5 py-0.5">{progressAlertCount}</span>}</button>\n'
    '        <button onClick={() => setFilter(\'done\')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === \'done\' ? \'bg-green-600 text-white\' : \'bg-slate-700 text-slate-300 hover:bg-slate-600\'}`}>\u7d0d\u54c1\u5b8c\u4e86\u5206</button>\n'
    '        <button onClick={() => setFilter(\'all\')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === \'all\' ? \'bg-blue-600 text-white\' : \'bg-slate-700 text-slate-300 hover:bg-slate-600\'}`}>\u5168\u4ef6\u8868\u793a</button>'
)

c = c.replace(old_buttons, new_buttons)

# 2. progressAlertCount を計算する useMemo を追加（allItemsから14日以内を数える）
# allItems stateを使う。なければloadStatsで全件取得してるstatsを活用
# allAssigneesの直後にprogress用の件数計算を追加
old_state = "  const [allAssignees, setAllAssignees] = useState<string[]>([])"
new_state = (
    "  const [allAssignees, setAllAssignees] = useState<string[]>([])\n"
    "  const [allItems, setAllItems] = useState<DeliveryItem[]>([])"
)
if old_state in c and "allItems" not in c:
    c = c.replace(old_state, new_state)

# progressAlertCount 計算（allItemsから）
old_load_stats = "  const loadStats = async () => {\n    const res = await fetch('/api/delivery/items')\n    const d = await res.json()\n    const all: DeliveryItem[] = d.items || []"
new_load_stats = (
    "  const loadStats = async () => {\n"
    "    const res = await fetch('/api/delivery/items')\n"
    "    const d = await res.json()\n"
    "    const all: DeliveryItem[] = d.items || []\n"
    "    setAllItems(all)"
)
if old_load_stats in c:
    c = c.replace(old_load_stats, new_load_stats)

# progressAlertCount の計算（返却前）
# 「return (」の直前に追加
old_return = "  return (\n    <div"
new_return = (
    "  const progressAlertCount = allItems.filter(i => {\n"
    "    if (i.status === 'done') return false\n"
    "    const due = new Date(i.delivery_due_date)\n"
    "    const diff = (due.getTime() - Date.now()) / (1000 * 60 * 60 * 24)\n"
    "    return diff <= 14\n"
    "  }).length\n\n"
    "  return (\n    <div"
)
if old_return in c and "progressAlertCount" not in c:
    c = c.replace(old_return, new_return)

with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK')
