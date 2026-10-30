# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# progressAlertCount の計算を allItems ではなく loadStats後のデータから取得
# allItemsに入っているか確認するため、stats state に progressCount を追加する

# 現在: setStats({ total: all.length, lastImport })
# 変更: setStats({ total, lastImport, progressAlertCount })

old_stats_type = "const [stats, setStats] = useState<{ total: number; lastImport: string | null } | null>(null)"
new_stats_type = "const [stats, setStats] = useState<{ total: number; lastImport: string | null; progressAlertCount?: number } | null>(null)"

old_set_stats = "    setStats({ total: all.length, lastImport })"
new_set_stats = (
    "    const now = Date.now()\n"
    "    const pac = all.filter(i => {\n"
    "      if (i.status === 'done') return false\n"
    "      if (!i.delivery_due_date) return false\n"
    "      const diff = (new Date(i.delivery_due_date).getTime() - now) / (1000 * 60 * 60 * 24)\n"
    "      return diff <= 14\n"
    "    }).length\n"
    "    setStats({ total: all.length, lastImport, progressAlertCount: pac })"
)

# progressAlertCount の参照をstatsから取得に変更
old_pac = (
    "  const progressAlertCount = allItems.filter(i => {\n"
    "    if (i.status === 'done') return false\n"
    "    const due = new Date(i.delivery_due_date)\n"
    "    const diff = (due.getTime() - Date.now()) / (1000 * 60 * 60 * 24)\n"
    "    return diff <= 14\n"
    "  }).length"
)
new_pac = "  const progressAlertCount = stats?.progressAlertCount ?? 0"

if old_stats_type in c:
    c = c.replace(old_stats_type, new_stats_type)
    print('stats type updated')
if old_set_stats in c:
    c = c.replace(old_set_stats, new_set_stats)
    print('setStats updated')
if old_pac in c:
    c = c.replace(old_pac, new_pac)
    print('progressAlertCount updated')

with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
print('Done')
