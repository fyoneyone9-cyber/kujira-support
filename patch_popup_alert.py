# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. state追加
old_state = "  const [isStale, setIsStale] = useState<boolean>(false)"
new_state = (
    "  const [isStale, setIsStale] = useState<boolean>(false)\n"
    "  const [popupAlerts, setPopupAlerts] = useState<{client: string; reason: string; days: number}[]>([])\n"
    "  const [popupDismissed, setPopupDismissed] = useState(false)"
)
c = c.replace(old_state, new_state)

# 2. loadStats内でアラート計算（setStats直後に追加）
old_set_stats = "    setStats({ total: all.length, lastImport, progressAlertCount: pac })"
new_set_stats = (
    "    setStats({ total: all.length, lastImport, progressAlertCount: pac })\n"
    "    // 10\u65e5\u4ee5\u5185\u30a2\u30e9\u30fc\u30c8\u306e\u53ce\u96c6\n"
    "    const now2 = Date.now()\n"
    "    const alerts: {client: string; reason: string; days: number}[] = []\n"
    "    all.forEach(i => {\n"
    "      if (i.status === 'done') return\n"
    "      const client = i.client_name || ''\n"
    "      const dueDiff = i.delivery_due_date ? Math.ceil((new Date(i.delivery_due_date).getTime() - now2) / 86400000) : null\n"
    "      if (dueDiff !== null && dueDiff <= 10)\n"
    "        alerts.push({ client, reason: '\u7d0d\u671f', days: dueDiff })\n"
    "      if (i.worker_needed && i.work_date) {\n"
    "        const wDiff = Math.ceil((new Date(i.work_date).getTime() - now2) / 86400000)\n"
    "        if (wDiff <= 10)\n"
    "          alerts.push({ client, reason: '\u4f5c\u696d\u65e5', days: wDiff })\n"
    "      }\n"
    "    })\n"
    "    alerts.sort((a, b) => a.days - b.days)\n"
    "    if (alerts.length > 0) setPopupAlerts(alerts)"
)
c = c.replace(old_set_stats, new_set_stats)

# 3. ポップアップUI（return直前の progressAlertCount定義の後に追加）
# return ( の直前に挿入
popup_jsx = (
    "  // 10\u65e5\u4ee5\u5185\u30a2\u30e9\u30fc\u30c8\u30dd\u30c3\u30d7\u30a2\u30c3\u30d7\n"
    "  const AlertPopup = popupAlerts.length > 0 && !popupDismissed ? (\n"
    "    <div className=\"fixed bottom-5 right-5 z-50 bg-slate-800 border border-red-500 rounded-xl shadow-2xl p-4 w-80 animate-in slide-in-from-bottom-4\">\n"
    "      <div className=\"flex items-center justify-between mb-3\">\n"
    "        <span className=\"text-red-400 font-bold text-sm\">\u26a0\ufe0f 10\u65e5\u4ee5\u5185\u306e\u4ef6 ({popupAlerts.length}\u4ef6)</span>\n"
    "        <button onClick={() => setPopupDismissed(true)} className=\"text-slate-400 hover:text-white text-lg leading-none\">\u00d7</button>\n"
    "      </div>\n"
    "      <div className=\"space-y-1.5 max-h-60 overflow-y-auto\">\n"
    "        {popupAlerts.map((a, idx) => (\n"
    "          <div key={idx} className={`flex items-center gap-2 text-xs rounded px-2 py-1 ${a.days <= 3 ? 'bg-red-900/60 text-red-200' : a.days <= 7 ? 'bg-orange-900/60 text-orange-200' : 'bg-slate-700 text-slate-300'}`}>\n"
    "            <span className=\"font-bold w-12 shrink-0\">{a.days <= 0 ? '\u671f\u9650\u8d85\u904e' : `${a.days}\u65e5\u5f8c`}</span>\n"
    "            <span className=\"shrink-0 text-slate-400\">{a.reason}</span>\n"
    "            <span className=\"truncate\">{a.client}</span>\n"
    "          </div>\n"
    "        ))}\n"
    "      </div>\n"
    "      <button onClick={() => { setFilter('progress'); setPopupDismissed(true) }} className=\"mt-3 w-full py-1.5 bg-yellow-700 hover:bg-yellow-600 text-white text-xs rounded-lg\">\u7d0d\u54c1\u7ba1\u7406\uff08\u9032\u884c\u4e2d\uff09\u3092\u958b\u304f</button>\n"
    "    </div>\n"
    "  ) : null\n\n"
)

c = c.replace("  const progressAlertCount = stats?.progressAlertCount ?? 0\n\n  return (",
              "  const progressAlertCount = stats?.progressAlertCount ?? 0\n\n" + popup_jsx + "  return (")

# 4. AlertPopupをreturn内の最後に追加（</div>の前）
# 最後の閉じタグ直前に挿入
c = c.rstrip()
if c.endswith('\n)'):
    c = c[:-2] + '\n      {AlertPopup}\n    </div>\n  )\n'

with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done')
