import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, encoding='utf-8') as f:
    content = f.read()

# 1. ヒアリング折りたたみ: IIFEとbutton+getElementById → div role=button + state
old1 = """                      {/* ヒアリングシートナビ（折りたたみ） */}
                      {(() => {
                        const [hOpen, setHOpen] = [
                          (it.dashboard_todos?.['_hearing_open'] as boolean) ?? false,
                          (v: boolean) => saveTodoKey(it.id, it.dashboard_todos, '_hearing_open', v ? '1' : '')
                        ]
                        return null // state管理はdiv外でやるのでここはplaceholder
                      })()}
                      <div className={`rounded-lg border ${hearingUrl ? 'border-purple-800' : 'border-slate-600'}`}>
                        <button
                          onClick={() => {
                            const key = `_hearing_open_${it.id}`
                            const el = document.getElementById(key)
                            if (el) el.style.display = el.style.display === 'none' ? '' : 'none'
                          }}
                          className={`w-full flex items-center gap-2 px-3 py-2 text-left rounded-lg ${hearingUrl ? 'bg-purple-950/40 hover:bg-purple-950/60' : 'bg-slate-800/50 hover:bg-slate-800'}`}
                        >
                          <span className="text-sm text-slate-300 font-bold">📋 ヒアリングシート</span>
                          {hearingUrl
                            ? <span className="text-purple-300 text-xs">登録済み</span>
                            : hearingSkip
                              ? <span className="text-xs text-slate-500">スキップ済み</span>
                              : <span className="text-xs text-orange-300 font-bold animate-pulse">⚠️ 未登録</span>
                          }
                          <span className="ml-auto text-slate-500 text-xs">▼ 開く</span>
                        </button>
                        <div id={`_hearing_open_${it.id}`} style={{display:'none'}} className="px-3 pb-3 space-y-2">"""

new1 = """                      {/* ヒアリングシートナビ（折りたたみ） */}
                      <div className={`rounded-lg border ${hearingUrl ? 'border-purple-800' : 'border-slate-600'}`}>
                        <div
                          role="button"
                          onClick={() => toggleSection(`hearing_${it.id}`)}
                          className={`flex items-center gap-2 px-3 py-2 cursor-pointer rounded-lg ${hearingUrl ? 'bg-purple-950/40 hover:bg-purple-950/60' : 'bg-slate-800/50 hover:bg-slate-800'}`}
                        >
                          <span className="text-sm text-slate-300 font-bold">📋 ヒアリングシート</span>
                          {hearingUrl
                            ? <span className="text-purple-300 text-xs">登録済み</span>
                            : hearingSkip
                              ? <span className="text-xs text-slate-500">スキップ済み</span>
                              : <span className="text-xs text-orange-300 font-bold animate-pulse">⚠️ 未登録</span>
                          }
                          <span className="ml-auto text-slate-500 text-xs">{openSections[`hearing_${it.id}`] ? '▲ 閉じる' : '▼ 開く'}</span>
                        </div>
                        {openSections[`hearing_${it.id}`] && <div className="px-3 pb-3 space-y-2">"""

# 2. 閉じタグ修正
old2 = """                        </div>{/* /_hearing_open div */}
                      </div>{/* /hearing折りたたみ外枠 */}"""
new2 = """                        </div>}{/* /hearing折りたたみ内 */}
                      </div>{/* /hearing折りたたみ外枠 */}"""

# 3. worker折りたたみのgetElementById
old3 = """                          const el = document.getElementById(`_worker_open_${it.id}`)
                          if (el) el.style.display = el.style.display === 'none' ? '' : 'none'"""
new3 = """                          toggleSection(`worker_${it.id}`)"""

# 4. worker open div
old4 = """                      <div id={`_worker_open_${it.id}`} style={{display:'none'}}>"""
new4 = """                      {openSections[`worker_${it.id}`] && <div>"""

# 5. worker close div
old5 = """                      </div>{/* /_worker_open */}"""
new5 = """                      </div>}{/* /_worker_open */}"""

changes = [(old1, new1), (old2, new2), (old3, new3), (old4, new4), (old5, new5)]
for old, new in changes:
    if old in content:
        content = content.replace(old, new)
        print(f'OK: replaced {repr(old[:60])}...')
    else:
        print(f'NOT FOUND: {repr(old[:80])}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('done')
