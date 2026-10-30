path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# toggleJitboxOrdered を 680行目付近（saveWorkDate の直前）に挿入
toggle_fn_lines = [
    '\n',
    '  const toggleJitboxOrdered = async (it: DeliveryItem) => {\n',
    '    if (blockIfLocked(it)) return\n',
    "    const next = !it.jitbox_ordered\n",
    "    const msg = next ? `\u300c${it.client_name}\u300dのJITBOX手配を\u300c手配済み\u300dにしますか？` : `\u300c${it.client_name}\u300dのJITBOX手配を\u300c未手配\u300dに戻しますか？`\n",
    '    if (!window.confirm(msg)) return\n',
    '    setItems(prev => prev.map(p => p.id === it.id ? { ...p, jitbox_ordered: next } : p))\n',
    '    await fetch(\'/api/delivery/items\', {\n',
    "      method: 'PATCH',\n",
    "      headers: { 'Content-Type': 'application/json' },\n",
    '      body: JSON.stringify({ id: it.id, jitbox_ordered: next })\n',
    '    })\n',
    '  }\n',
    '\n',
]

# line 681 (0-indexed: 680) の直前に挿入
insert_pos = 680  # "  // 作業日を保存" の行
lines = lines[:insert_pos] + toggle_fn_lines + lines[insert_pos:]

# JSXブロック：作業員セクションの直前に挿入
# 作業員セクションは "worker_needed" の flex div の直前
jitbox_jsx_lines = [
    '                      {/* JITBOX\u914d\u9001\u60c5\u5831 */}\n',
    '                      {hasJitbox(it) && (() => {\n',
    '                        const jit = getJitboxLeadDays(it.install_address)\n',
    '                        const today = new Date(); today.setHours(0,0,0,0)\n',
    '                        const due = new Date(it.delivery_due_date); due.setHours(0,0,0,0)\n',
    '                        const plainLeft = Math.ceil((due.getTime() - today.getTime()) / 86400000)\n',
    '                        const deadline = new Date(due); deadline.setDate(deadline.getDate() - jit.days - 1)\n',
    "                        const deadlineStr = deadline.toISOString().slice(0, 10)\n",
    '                        const daysToDeadline = Math.ceil((deadline.getTime() - today.getTime()) / 86400000)\n',
    '                        const isUrgent = daysToDeadline <= 3\n',
    '                        const isOverdue = daysToDeadline < 0\n',
    '                        return (\n',
    '                          <div className={`flex flex-col gap-2 mt-2 pt-2 border-t ${isOverdue ? \'border-red-500\' : isUrgent ? \'border-orange-500\' : \'border-slate-700/50\'}`}>\n',
    '                            <div className={`flex flex-col gap-1.5 px-3 py-2 rounded-lg ${isOverdue ? \'bg-red-950/50 border border-red-500\' : isUrgent ? \'bg-orange-950/50 border border-orange-500\' : \'bg-slate-800/60 border border-slate-700\'}`}>\n',
    '                              <div className="flex items-center gap-2 flex-wrap">\n',
    '                                <span className="text-lg font-bold text-white">\U0001f69a JITBOX\u914d\u9001\u60c5\u5831\uff08\u5927\u962a\u767a\uff09</span>\n',
    '                                {isOverdue && <span className="text-sm px-2 py-0.5 rounded-full bg-red-600 text-white font-bold">\u624b\u914d\u671f\u9650\u8d85\u904e\uff01</span>}\n',
    '                                {!isOverdue && isUrgent && <span className="text-sm px-2 py-0.5 rounded-full bg-orange-500 text-white font-bold">\u624b\u914d\u671f\u9650\u307e\u3067{daysToDeadline}\u65e5</span>}\n',
    '                              </div>\n',
    '                              <div className="text-base text-slate-300 space-y-0.5">\n',
    '                                <p>\U0001f4e6 \u6240\u8981\u65e5\u6570\uff1a<strong className="text-white">{jit.days}\u65e5</strong> <span className="text-slate-400 text-sm">\uff08{jit.note}\uff09</span></p>\n',
    '                                <p>\u23f0 \u624b\u914d\u7de0\u3081\u5207\u308a\uff1a<strong className={isOverdue ? \'text-red-300\' : isUrgent ? \'text-orange-300\' : \'text-white\'}>{deadlineStr}</strong>\n',
    '                                  <span className="text-slate-400 ml-2 text-sm">\uff08{isOverdue ? `${-daysToDeadline}\u65e5\u8d85\u904e` : `\u6b8b${daysToDeadline}\u65e5`} \uff0f \u524d\u65e5\u307e\u3067\u306b\u624b\u914d\u5fc5\u8981\uff09</span>\n',
    '                                </p>\n',
    '                                <p className="text-slate-400 text-sm">\u26a0\ufe0f \u65e5\u795d\u307e\u305f\u304e\u30fb\u96e2\u5cf6\u30fb2\u6642\u9593\u5e45JIT\u6307\u5b9a\u306f\u5225\u9014\u78ba\u8a8d\u3002\u6642\u9593\u5916\u914d\u9054(18:01\uff5e20:00)\u306f+3,000\u5186\u524d\u5f8c\u3002</p>\n',
    '                              </div>\n',
    '                              <button\n',
    '                                onClick={() => toggleJitboxOrdered(it)}\n',
    '                                disabled={!!it.locked}\n',
    "                                className={`self-start text-base px-4 py-1.5 rounded-full font-bold border transition-colors whitespace-nowrap ${it.jitbox_ordered ? 'bg-green-700 border-green-500 text-white' : 'bg-slate-700/60 border-slate-600 text-slate-300 hover:bg-slate-600'} ${it.locked ? 'opacity-50 cursor-not-allowed' : ''}`}\n",
    '                              >\n',
    '                                {it.jitbox_ordered ? \'\u2705 JITBOX\u624b\u914d\u6e08\u307f\' : \'\u2610 JITBOX\u624b\u914d\u6e08\u307f\u306b\u3059\u308b\'}\n',
    '                              </button>\n',
    '                            </div>\n',
    '                          </div>\n',
    '                        )\n',
    '                      })()}\n',
    '\n',
]

# 作業員セクション行を探す（"worker_needed" を含む div の flex行）
worker_section_keyword = 'flex flex-col gap-2 mt-2 pt-2 border-t border-slate-700/50'
insert_jsx_pos = None
for i, line in enumerate(lines):
    if worker_section_keyword in line:
        insert_jsx_pos = i
        break

if insert_jsx_pos:
    lines = lines[:insert_jsx_pos] + jitbox_jsx_lines + lines[insert_jsx_pos:]
    print(f'Inserted JITBOX JSX at line {insert_jsx_pos}')
else:
    print('ERROR: JSX insert position not found')

with open(path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print('Done.')
