'use client'

import { useEffect, useState } from 'react'

export default function BreakTimer() {
  const [startTime, setStartTime] = useState('')
  const [remaining, setRemaining] = useState<number | null>(null) // seconds
  const [active, setActive] = useState(false)
  const [ended, setEnded] = useState(false)

  // ページ読み込み時にlocalStorageから復元
  useEffect(() => {
    const saved = localStorage.getItem('breakTimer')
    if (saved) {
      const { endTs } = JSON.parse(saved)
      const diff = Math.floor((endTs - Date.now()) / 1000)
      if (diff > 0) {
        setRemaining(diff)
        setActive(true)
      } else {
        localStorage.removeItem('breakTimer')
      }
    }
  }, [])

  // カウントダウン
  useEffect(() => {
    if (!active) return
    const id = setInterval(() => {
      setRemaining(prev => {
        if (prev === null || prev <= 1) {
          clearInterval(id)
          setActive(false)
          setEnded(true)
          localStorage.removeItem('breakTimer')
          return 0
        }
        return prev - 1
      })
    }, 1000)
    return () => clearInterval(id)
  }, [active])

  const handleStart = () => {
    if (!startTime) return
    const [h, m] = startTime.split(':').map(Number)
    const now = new Date()
    const start = new Date(now)
    start.setHours(h, m, 0, 0)
    // 未来の場合はそのまま、過去なら今日と見なす
    const endTs = start.getTime() + 60 * 60 * 1000
    const diff = Math.floor((endTs - Date.now()) / 1000)
    if (diff <= 0) {
      alert('入力した時刻が1時間以上前です。現在時刻から1時間でスタートします。')
      const nowEndTs = Date.now() + 60 * 60 * 1000
      localStorage.setItem('breakTimer', JSON.stringify({ endTs: nowEndTs }))
      setRemaining(3600)
    } else {
      localStorage.setItem('breakTimer', JSON.stringify({ endTs }))
      setRemaining(diff)
    }
    setActive(true)
    setEnded(false)
  }

  const handleReset = () => {
    setActive(false)
    setRemaining(null)
    setEnded(false)
    setStartTime('')
    localStorage.removeItem('breakTimer')
  }

  // 現在時刻をデフォルト入力
  const setNow = () => {
    const now = new Date()
    const h = String(now.getHours()).padStart(2, '0')
    const m = String(now.getMinutes()).padStart(2, '0')
    setStartTime(`${h}:${m}`)
  }

  const fmt = (s: number) => {
    const m = Math.floor(s / 60)
    const sec = s % 60
    return `${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`
  }

  const pct = remaining !== null ? Math.min(100, (remaining / 3600) * 100) : 0
  const isWarning = remaining !== null && remaining <= 300 // 5分以内

  return (
    <div className={`bg-slate-800 rounded-2xl border p-5 mb-6 transition-colors ${
      ended ? 'border-red-500 animate-pulse' : isWarning && active ? 'border-yellow-500' : 'border-slate-700'
    }`}>
      <h2 className="text-base font-semibold text-white mb-4">⏱️ 休憩タイマー</h2>

      {ended ? (
        <div className="text-center py-4">
          <p className="text-3xl mb-2">🔔</p>
          <p className="text-red-400 text-lg font-bold">休憩終了！</p>
          <p className="text-slate-400 text-sm mt-1">1時間が経過しました</p>
          <button onClick={handleReset} className="mt-4 px-6 py-2 bg-slate-700 hover:bg-slate-600 rounded-xl text-white text-sm font-medium transition-colors">
            リセット
          </button>
        </div>
      ) : active && remaining !== null ? (
        <div>
          {/* プログレスバー */}
          <div className="relative h-3 bg-slate-700 rounded-full mb-4 overflow-hidden">
            <div
              className={`absolute left-0 top-0 h-full rounded-full transition-all ${isWarning ? 'bg-yellow-500' : 'bg-green-500'}`}
              style={{ width: `${pct}%` }}
            />
          </div>
          <div className="flex items-center justify-between">
            <div>
              <p className={`text-4xl font-mono font-bold ${isWarning ? 'text-yellow-400' : 'text-green-400'}`}>
                {fmt(remaining)}
              </p>
              <p className="text-slate-500 text-xs mt-1">残り時間</p>
            </div>
            <button onClick={handleReset} className="px-4 py-2 bg-slate-700 hover:bg-slate-600 rounded-xl text-slate-300 text-sm font-medium transition-colors">
              リセット
            </button>
          </div>
          {isWarning && (
            <p className="text-yellow-400 text-xs mt-3 font-medium">⚠️ まもなく休憩終了です</p>
          )}
        </div>
      ) : (
        <div className="flex items-end gap-3 flex-wrap">
          <div>
            <p className="text-xs text-slate-500 mb-1">休憩開始時刻</p>
            <input
              type="time"
              value={startTime}
              onChange={e => setStartTime(e.target.value)}
              className="px-3 py-2.5 bg-slate-700 border border-slate-600 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-green-500"
            />
          </div>
          <button
            onClick={setNow}
            className="px-3 py-2.5 bg-slate-700 hover:bg-slate-600 border border-slate-600 rounded-xl text-slate-300 text-sm transition-colors"
          >
            今すぐ
          </button>
          <button
            onClick={handleStart}
            disabled={!startTime}
            className="px-5 py-2.5 bg-green-600 hover:bg-green-500 disabled:opacity-40 disabled:cursor-not-allowed rounded-xl text-white text-sm font-bold transition-colors"
          >
            スタート
          </button>
        </div>
      )}
    </div>
  )
}
