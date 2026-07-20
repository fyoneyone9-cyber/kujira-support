'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { createClient } from '@/lib/supabase/client'

type Mode = 'idle' | 'summarizing' | 'converting' | 'done_summary' | 'done_manual'

export default function LogAiPanel({
  logId,
  title,
  content,
}: {
  logId: string
  title: string | null
  content: string
}) {
  const router = useRouter()
  const [mode, setMode] = useState<Mode>('idle')
  const [result, setResult] = useState('')
  const [error, setError] = useState('')

  const summarize = async () => {
    setMode('summarizing')
    setError('')
    setResult('')
    try {
      const res = await fetch('/api/ai/summarize-log', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content, title }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error)
      setResult(data.summary)
      setMode('done_summary')
    } catch (e) {
      setError(e instanceof Error ? e.message : 'エラーが発生しました')
      setMode('idle')
    }
  }

  const toManual = async () => {
    setMode('converting')
    setError('')
    setResult('')
    try {
      const res = await fetch('/api/ai/to-manual', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content, title }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error)
      setResult(data.manual)
      setMode('done_manual')
    } catch (e) {
      setError(e instanceof Error ? e.message : 'エラーが発生しました')
      setMode('idle')
    }
  }

  const saveAsManual = async () => {
    // マニュアルタイトルを抽出
    const titleMatch = result.match(/## マニュアルタイトル\n(.+)/)
    const manualTitle = titleMatch?.[1]?.trim() ?? title ?? 'マニュアル'

    const supabase = createClient()
    const { data: { user } } = await supabase.auth.getUser()
    const { data, error } = await supabase.from('manuals').insert({
      title: manualTitle,
      content: result,
      created_by: user?.id,
    }).select().single()

    if (error) { setError('保存失敗: ' + error.message); return }
    router.push(`/manuals/${data.id}`)
  }

  const isLoading = mode === 'summarizing' || mode === 'converting'

  return (
    <div className="mb-6 space-y-3">
      {/* Buttons */}
      <div className="flex gap-3">
        <button
          onClick={summarize}
          disabled={isLoading}
          className="flex items-center gap-2 px-4 py-2.5 bg-purple-600/20 hover:bg-purple-600/30 border border-purple-500/40 text-purple-300 text-sm font-medium rounded-xl transition-colors disabled:opacity-50"
        >
          {mode === 'summarizing' ? (
            <><span className="animate-spin">⟳</span> 要約中...</>
          ) : (
            <>✨ AI要約</>
          )}
        </button>
        <button
          onClick={toManual}
          disabled={isLoading}
          className="flex items-center gap-2 px-4 py-2.5 bg-green-600/20 hover:bg-green-600/30 border border-green-500/40 text-green-300 text-sm font-medium rounded-xl transition-colors disabled:opacity-50"
        >
          {mode === 'converting' ? (
            <><span className="animate-spin">⟳</span> 変換中...</>
          ) : (
            <>📋 マニュアル化</>
          )}
        </button>
        {(mode === 'done_summary' || mode === 'done_manual') && (
          <button
            onClick={() => { setMode('idle'); setResult('') }}
            className="px-4 py-2.5 bg-slate-700 hover:bg-slate-600 text-slate-300 text-sm rounded-xl transition-colors"
          >
            閉じる
          </button>
        )}
      </div>

      {/* Error */}
      {error && (
        <p className="text-red-400 text-sm bg-red-400/10 px-4 py-3 rounded-xl">{error}</p>
      )}

      {/* Result */}
      {result && (
        <div className="bg-slate-800 rounded-2xl border border-slate-600 overflow-hidden">
          <div className="flex items-center justify-between px-5 py-3 border-b border-slate-700 bg-slate-700/50">
            <p className="text-sm font-medium text-white">
              {mode === 'done_summary' ? '✨ AI要約結果' : '📋 マニュアル案'}
            </p>
            {mode === 'done_manual' && (
              <button
                onClick={saveAsManual}
                className="px-3 py-1.5 bg-green-600 hover:bg-green-500 text-white text-xs font-medium rounded-lg transition-colors"
              >
                マニュアルとして保存
              </button>
            )}
          </div>
          <div className="p-5">
            <pre className="text-slate-200 text-sm leading-relaxed whitespace-pre-wrap">
              {result}
            </pre>
          </div>
        </div>
      )}
    </div>
  )
}
