# -*- coding: utf-8 -*-
path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. stateにrebuildStateとisStaleを追加
old_state = "  const [searchQuery, setSearchQuery] = useState<string>('')\n"
new_state = """  const [searchQuery, setSearchQuery] = useState<string>('')
  const [rebuildState, setRebuildState] = useState<'idle'|'running'|'success'|'failed'>('idle')
  const [isStale, setIsStale] = useState<boolean>(false)
"""
content = content.replace(old_state, new_state, 1)

# 2. useEffect群の後にtriggerRebuild関数を追加
old_effect = "  useEffect(() => { load() }, [filter, assigneeFilter])\n  useEffect(() => { loadStats() }, [])"
new_effect = """  useEffect(() => { load() }, [filter, assigneeFilter])
  useEffect(() => { loadStats() }, [])
  useEffect(() => {
    const checkStale = async () => {
      try { const r = await fetch('/api/admin/build-status'); const d = await r.json(); setIsStale(!!d.isStale) } catch {}
    }
    checkStale(); const t = setInterval(checkStale, 60000); return () => clearInterval(t)
  }, [])

  const triggerRebuild = async () => {
    if (!window.confirm('コードの変更をビルドしてサーバーを再起動します。1〜2分かかります。実行しますか？')) return
    setRebuildState('running')
    try { await fetch('/api/admin/rebuild', { method: 'POST' }) } catch {}
    const poll = setInterval(async () => {
      try {
        const r = await fetch('/api/admin/rebuild/status'); const d = await r.json()
        if (d.done) { clearInterval(poll); setRebuildState(d.success ? 'success' : 'failed'); if (d.success) setTimeout(() => setRebuildState('idle'), 8000) }
      } catch {}
    }, 4000)
    setTimeout(() => clearInterval(poll), 3 * 60 * 1000)
  }"""
content = content.replace(old_effect, new_effect, 1)

# 3. ヘッダー部分に更新ボタンを追加
old_header = '          <h1 className="text-2xl font-bold text-white">IoT製品 納品予定アラート</h1>'
new_header = '''          <h1 className="text-2xl font-bold text-white">IoT製品 納品予定アラート</h1>
          <button
            onClick={triggerRebuild}
            disabled={rebuildState === 'running'}
            className={`px-3 py-1 text-sm font-bold rounded-lg inline-flex items-center gap-1 disabled:opacity-70 ${
              rebuildState === 'success' ? 'bg-green-700 text-white' :
              rebuildState === 'failed' ? 'bg-red-700 text-white' :
              rebuildState === 'running' ? 'bg-amber-700 text-white' :
              'bg-slate-700 hover:bg-slate-600 text-white'
            }`}
          >
            {rebuildState === 'running' && '⏳ ビルド中...'}
            {rebuildState === 'success' && '✅ 反映完了'}
            {rebuildState === 'failed' && '❌ ビルド失敗'}
            {rebuildState === 'idle' && '🔧 更新を反映'}
          </button>
          {isStale && <span className="text-xs text-amber-400 font-bold animate-pulse">⚠️ 未反映の変更あり</span>}'''
content = content.replace(old_header, new_header, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done.')
