path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# toggleJitboxOrdered 関数を saveWorkDate の直前に追加
toggle_fn = """
  const toggleJitboxOrdered = async (it: DeliveryItem) => {
    if (blockIfLocked(it)) return
    const next = !it.jitbox_ordered
    const msg = next ? `「${it.client_name}」のJITBOX手配を「手配済み」にしますか？` : `「${it.client_name}」のJITBOX手配を「未手配」に戻しますか？`
    if (!window.confirm(msg)) return
    setItems(prev => prev.map(p => p.id === it.id ? { ...p, jitbox_ordered: next } : p))
    await fetch('/api/delivery/items', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: it.id, jitbox_ordered: next })
    })
  }

"""

target_fn = '  // 作業日を保存'
if target_fn in content:
    content = content.replace(target_fn, toggle_fn + target_fn, 1)
    print('Inserted toggleJitboxOrdered OK')
else:
    print('ERROR: toggleJitboxOrdered target not found')

# JSXブロック：作業員セクションの直前に挿入
jitbox_jsx = """
                      {/* JITBOX配送情報（備考にJITBOXが含まれる場合に表示） */}
                      {hasJitbox(it) && (() => {
                        const jit = getJitboxLeadDays(it.install_address)
                        const today = new Date(); today.setHours(0,0,0,0)
                        const due = new Date(it.delivery_due_date); due.setHours(0,0,0,0)
                        const plainLeft = Math.ceil((due.getTime() - today.getTime()) / 86400000)
                        // 手配締め切り = 納品予定日 - リードタイム - 1（前日までに手配必要）
                        const deadline = new Date(due); deadline.setDate(deadline.getDate() - jit.days - 1)
                        const deadlineStr = deadline.toISOString().slice(0, 10)
                        const daysToDeadline = Math.ceil((deadline.getTime() - today.getTime()) / 86400000)
                        const isUrgent = daysToDeadline <= 3
                        const isOverdue = daysToDeadline < 0
                        return (
                          <div className={`flex flex-col gap-2 mt-2 pt-2 border-t ${isOverdue ? 'border-red-500' : isUrgent ? 'border-orange-500' : 'border-slate-700/50'}`}>
                            <div className={`flex flex-col gap-1.5 px-3 py-2 rounded-lg ${isOverdue ? 'bg-red-950/50 border border-red-500' : isUrgent ? 'bg-orange-950/50 border border-orange-500' : 'bg-slate-800/60 border border-slate-700'}`}>
                              <div className="flex items-center gap-2 flex-wrap">
                                <span className="text-lg font-bold text-white">🚚 JITBOX配送情報（大阪発）</span>
                                {isOverdue && <span className="text-sm px-2 py-0.5 rounded-full bg-red-600 text-white font-bold">手配期限超過！</span>}
                                {!isOverdue && isUrgent && <span className="text-sm px-2 py-0.5 rounded-full bg-orange-500 text-white font-bold">手配期限まで{daysToDeadline}日</span>}
                              </div>
                              <div className="text-base text-slate-300 space-y-0.5">
                                <p>📦 所要日数：<strong className="text-white">{jit.days}日</strong> <span className="text-slate-400 text-sm">（{jit.note}）</span></p>
                                <p>⏰ 手配締め切り：<strong className={isOverdue ? 'text-red-300' : isUrgent ? 'text-orange-300' : 'text-white'}>{deadlineStr}</strong>
                                  <span className="text-slate-400 ml-2 text-sm">（{isOverdue ? `${-daysToDeadline}日超過` : `残${daysToDeadline}日`} ／ 前日までに手配必要）</span>
                                </p>
                                <p className="text-slate-400 text-sm">⚠️ 日祝またぎ・離島・2時間幅JIT指定は別途確認。時間外配達(18:01〜20:00)は+3,000円前後。</p>
                              </div>
                              <button
                                onClick={() => toggleJitboxOrdered(it)}
                                disabled={!!it.locked}
                                className={`self-start text-base px-4 py-1.5 rounded-full font-bold border transition-colors whitespace-nowrap ${it.jitbox_ordered ? 'bg-green-700 border-green-500 text-white' : 'bg-slate-700/60 border-slate-600 text-slate-300 hover:bg-slate-600'} ${it.locked ? 'opacity-50 cursor-not-allowed' : ''}`}
                              >
                                {it.jitbox_ordered ? '✅ JITBOX手配済み' : '☐ JITBOX手配済みにする'}
                              </button>
                            </div>
                          </div>
                        )
                      })()}

"""

# 作業員管理セクションの直前に挿入
worker_marker = '{/* 作業員管理'
if worker_marker in content:
    content = content.replace(worker_marker, jitbox_jsx + worker_marker, 1)
    print('Inserted JITBOX JSX block OK')
else:
    print(f'ERROR: JSX target not found. Searching partial...')
    import re
    matches = [(m.start(), content[m.start():m.start()+50]) for m in re.finditer(r'\{/\* ', content)]
    for pos, snip in matches[-10:]:
        print(f'  {pos}: {repr(snip)}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
