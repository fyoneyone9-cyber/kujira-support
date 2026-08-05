'use client'

import { useState } from 'react'

const DEFAULT_START = '09:00'
const DEFAULT_END = '18:00'
const DEFAULT_BREAK = '1.0'


// HH:MM × 2 → 差を時間（小数）で返す
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
  const [slackContent, setSlackContent] = useState('')
  const [startTime, setStartTime] = useState(DEFAULT_START)
  const [endTime, setEndTime] = useState(DEFAULT_END)
  const [breakTime, setBreakTime] = useState(DEFAULT_BREAK)

  // 実労働時間は自動計算（手入力なし）
  const workTime = calcWork(startTime, endTime, breakTime)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [nippouBody, setNippouBody] = useState('')
  const [copied, setCopied] = useState(false)

  const generate = async () => {
    if (!slackContent.trim()) return
    setLoading(true)
    setError('')
    setNippouBody('')
    setCopied(false)

    try {
      const res = await fetch('/api/ai/nippou', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: slackContent }),
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
        <p className="text-slate-400 text-sm mt-1">Slackのやり取りを貼り付けて、日報を自動生成します。</p>
      </div>

      <div className="space-y-6">
        {/* 勤務状況 */}
        <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700 space-y-4">
          <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wide">勤務状況</h2>
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs text-slate-400 mb-1">勤務開始</label>
              <input
                type="time"
                value={startTime}
                onChange={(e) => setStartTime(e.target.value)}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">勤務終了</label>
              <input
                type="time"
                value={endTime}
                onChange={(e) => setEndTime(e.target.value)}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">休憩時間（h）</label>
              <input
                type="number"
                step="0.5"
                min="0"
                value={breakTime}
                onChange={(e) => setBreakTime(e.target.value)}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-xs text-slate-400 mb-1">実労働時間（h）<span className="ml-1 text-blue-400">自動計算</span></label>
              <div className={`w-full px-3 py-2 rounded-xl text-sm font-bold border ${
                workTime ? 'bg-blue-900/40 border-blue-700 text-blue-300' : 'bg-slate-700 border-slate-600 text-slate-500'
              }`}>
                {workTime ? `${workTime} h` : '— h'}
              </div>
            </div>
          </div>
        </div>

        {/* Slack入力 */}
        <div className="bg-slate-800 rounded-2xl p-6 border border-slate-700 space-y-3">
          <h2 className="text-sm font-semibold text-slate-300 uppercase tracking-wide">Slackのやり取り</h2>
          <textarea
            value={slackContent}
            onChange={(e) => setSlackContent(e.target.value)}
            placeholder="今日のSlackのやり取りをここにコピペしてください..."
            rows={12}
            className="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 text-sm font-mono resize-y"
          />
          <p className="text-xs text-slate-500">
            {slackContent.length > 0 ? `${slackContent.length} 文字` : ''}
          </p>
        </div>

        {/* 生成ボタン */}
        <button
          onClick={generate}
          disabled={loading || !slackContent.trim()}
          className="w-full py-3 bg-blue-600 hover:bg-blue-500 disabled:bg-slate-600 disabled:cursor-not-allowed text-white font-medium rounded-xl transition-colors flex items-center justify-center gap-2"
        >
          {loading ? (
            <><span className="animate-spin inline-block">⟳</span> 日報を生成中...</>
          ) : (
            <>📝 日報を生成する</>
          )}
        </button>

        {/* エラー */}
        {error && (
          <p className="text-red-400 text-sm bg-red-400/10 px-4 py-3 rounded-xl">{error}</p>
        )}

        {/* 結果表示 */}
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
              <pre className="text-slate-200 text-sm leading-relaxed whitespace-pre-wrap">
                {fullNippou}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
