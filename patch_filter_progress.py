# -*- coding: utf-8 -*-
with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. 型定義
c = c.replace(
    "const [filter, setFilter] = useState<'alert' | 'all' | 'done'>('alert')",
    "const [filter, setFilter] = useState<'alert' | 'all' | 'progress' | 'done'>('alert')"
)

# 2. クライアント側フィルタロジック
c = c.replace(
    "    if (filter === 'done') data = data.filter(i => i.status === 'done')\n    if (filter !== 'done') data = data.filter(i => i.status !== 'done')",
    "    if (filter === 'done') data = data.filter(i => i.status === 'done')\n    else if (filter === 'progress') data = data.filter(i => i.status === 'active')\n    else data = data.filter(i => i.status !== 'done')"
)

# 3. ボタン追加（納品完了分の前に挿入）
old_btn = "        <button onClick={() => setFilter('done')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'done' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>\u7d0d\u54c1\u5b8c\u4e86\u5206</button>"
new_btn = (
    "        <button onClick={() => setFilter('progress')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'progress' ? 'bg-yellow-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>\u7d0d\u54c1\u7ba1\u7406\uff08\u9032\u884c\u4e2d\uff09</button>\n"
    "        <button onClick={() => setFilter('done')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'done' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>\u7d0d\u54c1\u5b8c\u4e86\u5206</button>"
)
c = c.replace(old_btn, new_btn)

with open(r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx', 'w', encoding='utf-8') as f:
    f.write(c)
print('OK')
