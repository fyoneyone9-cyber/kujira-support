'use client'

import { useState } from 'react'

const DEFAULT_START = '09:00'
const DEFAULT_END = '18:00'
const DEFAULT_BREAK = '1.0'
const SLOT_COUNT = 20

function calcWork(start: string, end: string, br: string): string {
  const [sh, sm] = start.split(':').map(Number)
  const [eh, em] = end.split(':').map(Number)
  const totalMin = (eh * 60 + em) - (sh * 60 + sm)
  if (isNaN(totalMin) || totalMin <= 0) return ''
  const workMin = totalMin - parseFloat(br || '0') * 60
  if (workMin <= 0) return '0.0'
  return (workMin / 60).toFixed(1)
}

export default function NippouPage() {
  const [startTime, setStartTime] = useState(DEFAULT_START)
  const [endTime, setEndTime]     = useState(DEFAULT_END)
  const [breakTime, setBreakTime] = useState(DEFAULT_BREAK)
  const workTime = calcWork(startTime, endTime, breakTime)

  // 20個のSlack貼り付け枠
  const [slots, setSlots] = useState<string[]>(Array(SLOT_COUNT).fill(''))

  const setSlot = (i: number, v: string) => {
    setSlots(prev => { const n = [...prev]; n[i] = v; return n })
  }
  const clearSlot = (i: number) => setSlot(i, '')

  // 入力済みスロットだけ結合
  const mergedContent = slots.filter(s => s.trim()).join('\n\n---\n\n')
  const filledCount   = slots.filter(s => s.trim()).length

  const [loading, setLoading]     = useState(false)
  const [error, setError]         = useState('')
  const [nippouBody, setNippouBody] = useState('')
  const [copied, setCopied]       = useState(false)

  const generate = async () => {
    if (!mergedContent) return
    setLoading(true); setError(''); setNippouBody(''); setCopied(false)
    try {
      const res = await fetch('/api/ai/nippou', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: mergedContent }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error)
      setNippouBody(data.nippou)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'エラーが発生しました')
    } finally {
      setLoading(false)
    }
  }

  const fullNippou = `## 【社内提出用】通常日報

勤務状況
- 勤務時間：${startTime} - ${endTime}
- 休憩時間：${breakTime}h
- 実労働時間：${workTime}h

${nippouBody}`

  const handleCopy = () => {
    navigator.clipboard.writeText(fullNippou)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="max-w-3xl">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-white">日報作成</h1>
        <p className="text-slate-400 text-sm mt-1">Slackのやり取りを最大20個貼り付けて、日報を自動生成します。</p>
      </div>

      <div className="space-y-6">

        {/* 勤務状況 */}
        <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700 space-y-4">
          <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wide">勤務状況</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs text-slate-400 mb-1">勤務開始</label>
              <input type="time" value={startTime} onChange={e => setStartTime(e.target.value)}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">勤務終了</label>
              <input type="time" value={endTime} onChange={e => setEndTime(e.target.value)}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">休憩時間（h）</label>
              <input type="number" step="0.5" min="0" value={breakTime} onChange={e => setBreakTime(e.target.value)}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500" />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">
                実労働時間（h）<span className="ml-1 text-blue-400">自動計算</span>
              </label>
              <div className={`w-full px-3 py-2 rounded-xl text-sm font-bold border ${
                workTime ? 'bg-blue-900/40 border-blue-700 text-blue-300' : 'bg-slate-700 border-slate-600 text-slate-500'
              }`}>
                {workTime ? `${workTime} h` : '— h'}
              </div>
            </div>
          </div>
        </div>

        {/* Slack 20枠 */}
        <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wide">Slackのやり取り</h2>
              <p className="text-xs text-slate-500 mt-0.5">各枠にコピペ → 「日報を生成する」で自動結合して日報化</p>
            </div>
            <div className="flex items-center gap-3">
              <span className="text-sm text-slate-400">
                <span className={filledCount > 0 ? 'text-blue-400 font-bold' : ''}>{filledCount}</span>
                <span className="text-slate-600"> / {SLOT_COUNT} 入力済み</span>
              </span>
              {filledCount > 0 && (
                <button
                  onClick={() => setSlots(Array(SLOT_COUNT).fill(''))}
                  className="text-xs text-red-400 hover:text-red-300 px-2 py-1 rounded-lg bg-red-950/30 border border-red-800/40"
                >
                  全クリア
                </button>
              )}
            </div>
          </div>

          <div className="space-y-3">
            {slots.map((slot, i) => (
              <div key={i} className="flex gap-2 items-start">
                {/* 番号バッジ */}
                <span className={`mt-2 flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold ${
                  slot.trim() ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-500'
                }`}>{i + 1}</span>

                {/* テキストエリア */}
                <textarea
                  value={slot}
                  onChange={e => setSlot(i, e.target.value)}
                  placeholder={`Slackのやり取り ${i + 1} 枠目…`}
                  rows={slot.trim() ? Math.min(6, slot.split('\n').length + 1) : 2}
                  className={`flex-1 px-3 py-2 rounded-xl text-sm font-mono resize-none focus:outline-none focus:ring-2 border transition-colors ${
                    slot.trim()
                      ? 'bg-slate-700 border-blue-700/60 text-white focus:ring-blue-500'
                      : 'bg-slate-700/50 border-slate-600 text-slate-300 placeholder-slate-600 focus:ring-blue-500'
                  }`}
                />

                {/* クリアボタン */}
                {slot.trim() && (
                  <button
                    onClick={() => clearSlot(i)}
                    className="mt-2 text-slate-500 hover:text-red-400 text-lg leading-none flex-shrink-0"
                    title="クリア"
                  >×</button>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* 生成ボタン */}
        <button
          onClick={generate}
          disabled={loading || filledCount === 0}
          className="w-full py-4 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-bold text-base rounded-xl transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <><span className="animate-spin inline-block">⟳</span> 日報を生成中…</>
          ) : (
            <>📝 {filledCount}件のやり取りを結合して日報を生成する</>
          )}
        </button>

        {error && (
          <p className="text-red-400 text-sm bg-red-400/10 px-4 py-3 rounded-xl">{error}</p>
        )}

        {/* 結果 */}
        {nippouBody && (
          <div className="bg-slate-800 rounded-2xl border border-slate-600 overflow-hidden">
            <div className="flex items-center justify-between px-5 py-3 border-b border-slate-700 bg-slate-700/50">
              <p className="text-sm font-medium text-white">📄 生成された日報</p>
              <button
                onClick={handleCopy}
                className="px-3 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-xs font-medium rounded-lg transition-colors"
              >
                {copied ? '✅ コピー済み' : '📋 コピー'}
              </button>
            </div>
            <div className="p-5">
              <pre className="text-slate-200 text-sm leading-relaxed whitespace-pre-wrap">{fullNippou}</pre>
            </div>
          </div>
        )}

      </div>
    </div>
  )
}
