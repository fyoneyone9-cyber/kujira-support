# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. popupAlerts 計算に assigneeFilter を反映
# loadStats内のアラート収集は全件から行い、表示時にフィルタする方が確実
# AlertPopup の filter を assigneeFilter でさらに絞る

old_popup_var = "  const AlertPopup = popupAlerts.length > 0 && !popupDismissed ? ("
new_popup_var = (
    "  const filteredPopupAlerts = assigneeFilter === 'all'\n"
    "    ? popupAlerts\n"
    "    : popupAlerts.filter(a => a.assignee === assigneeFilter)\n\n"
    "  const AlertPopup = filteredPopupAlerts.length > 0 && !popupDismissed ? ("
)
c = c.replace(old_popup_var, new_popup_var)

# 2. popupAlerts の型に assignee を追加
c = c.replace(
    "  const [popupAlerts, setPopupAlerts] = useState<{client: string; reason: string; days: number}[]>([])",
    "  const [popupAlerts, setPopupAlerts] = useState<{id: string; client: string; reason: string; days: number; assignee: string}[]>([])"
)

# 3. アラート収集に id と assignee を追加
c = c.replace(
    "      if (dueDiff !== null && dueDiff <= 10)\n"
    "        alerts.push({ client, reason: '\u7d0d\u671f', days: dueDiff })\n"
    "      if (i.worker_needed && i.work_date) {\n"
    "        const wDiff = Math.ceil((new Date(i.work_date).getTime() - now2) / 86400000)\n"
    "        if (wDiff <= 10)\n"
    "          alerts.push({ client, reason: '\u4f5c\u696d\u65e5', days: wDiff })\n"
    "      }",
    "      const assignee = i.assignee || ''\n"
    "      if (dueDiff !== null && dueDiff <= 10)\n"
    "        alerts.push({ id: i.id, client, reason: '\u7d0d\u671f', days: dueDiff, assignee })\n"
    "      if (i.worker_needed && i.work_date) {\n"
    "        const wDiff = Math.ceil((new Date(i.work_date).getTime() - now2) / 86400000)\n"
    "        if (wDiff <= 10)\n"
    "          alerts.push({ id: i.id, client, reason: '\u4f5c\u696d\u65e5', days: wDiff, assignee })\n"
    "      }"
)

# 4. ポップアップのリスト部分: popupAlerts → filteredPopupAlerts、クリックでスクロール
c = c.replace(
    "        {popupAlerts.map((a, idx) => (\n"
    "          <div key={idx} className={`flex items-center gap-2 text-xs rounded px-2 py-1 ${a.days <= 3 ? 'bg-red-900/60 text-red-200' : a.days <= 7 ? 'bg-orange-900/60 text-orange-200' : 'bg-slate-700 text-slate-300'}`}>\n"
    "            <span className=\"font-bold w-12 shrink-0\">{a.days <= 0 ? '\u671f\u9650\u8d85\u904e' : `${a.days}\u65e5\u5f8c`}</span>\n"
    "            <span className=\"shrink-0 text-slate-400\">{a.reason}</span>\n"
    "            <span className=\"truncate\">{a.client}</span>\n"
    "          </div>\n"
    "        ))}",
    "        {filteredPopupAlerts.map((a, idx) => (\n"
    "          <div key={idx}\n"
    "            onClick={() => {\n"
    "              setPopupDismissed(true)\n"
    "              setTimeout(() => {\n"
    "                const el = document.getElementById(`card-${a.id}`)\n"
    "                if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })\n"
    "              }, 100)\n"
    "            }}\n"
    "            className={`flex items-center gap-2 text-xs rounded px-2 py-1 cursor-pointer hover:opacity-80 ${a.days <= 3 ? 'bg-red-900/60 text-red-200' : a.days <= 7 ? 'bg-orange-900/60 text-orange-200' : 'bg-slate-700 text-slate-300'}`}>\n"
    "            <span className=\"font-bold w-12 shrink-0\">{a.days <= 0 ? '\u671f\u9650\u8d85\u904e' : `${a.days}\u65e5\u5f8c`}</span>\n"
    "            <span className=\"shrink-0 text-slate-400\">{a.reason}</span>\n"
    "            <span className=\"truncate\">{a.client}</span>\n"
    "          </div>\n"
    "        ))}"
)

# 5. 件数表示も filteredPopupAlerts に
c = c.replace(
    "<span className=\"text-red-400 font-bold text-sm\">\u26a0\ufe0f 10\u65e5\u4ee5\u5185\u306e\u4ef6 ({popupAlerts.length}\u4ef6)</span>",
    "<span className=\"text-red-400 font-bold text-sm\">\u26a0\ufe0f 10\u65e5\u4ee5\u5185\u306e\u4ef6 ({filteredPopupAlerts.length}\u4ef6)</span>"
)

# 6. 各カードに id を付与（スクロール先特定用）
# <div key={it.id} className="bg-slate-800... → id={`card-${it.id}`} を追加
# カードのトップdivを探す
c = c.replace(
    '          <div key={it.id} className="bg-slate-800',
    '          <div key={it.id} id={`card-${it.id}`} className="bg-slate-800'
)

with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done')
