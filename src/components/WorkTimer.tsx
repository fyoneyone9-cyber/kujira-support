'use client'

import { useEffect, useState } from 'react'

// 公休日: 日(0)・月(1)
const OFF_DAYS = [0, 1]
const WORK_HOUR = 9
const WORK_MIN = 0

function getStatus() {
  const now = new Date()
  const day = now.getDay()
  const h = now.getHours()
  const m = now.getMinutes()
  const s = now.getSeconds()

  if (OFF_DAYS.includes(day)) {
    return { type: 'off' as const, remaining: null }
  }

  const totalNowSec = h * 3600 + m * 60 + s
  const workStartSec = WORK_HOUR * 3600 + WORK_MIN * 60

  if (totalNowSec >= workStartSec) {
    // 勤務中
    const workedSec = totalNowSec - workStartSec
    return { type: 'working' as const, remaining: workedSec }
  } else {
    // 勤務前
    const remaining = workStartSec - totalNowSec
    return { type: 'before' as const, remaining }
  }
}

function fmt(s: number) {
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  const sec = s % 60
  if (h > 0) return `${h}時間${String(m).padStart(2, '0')}分`
  return `${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`
}

const DAY_NAMES = ['日', '月', '火', '水', '木', '金', '土']

export default function WorkTimer() {
  const [status, setStatus] = useState(getStatus)
  const [now, setNow] = useState(new Date())

  useEffect(() => {
    const id = setInterval(() => {
      setStatus(getStatus())
      setNow(new Date())
    }, 1000)
    return () => clearInterval(id)
  }, [])

  const day = now.getDay()
  const dayLabel = DAY_NAMES[day]
  const isOff = OFF_DAYS.includes(day)

  return (
    <div className={`rounded-2xl border p-5 mb-3 ${
      isOff ? 'bg-slate-800/50 border-slate-700' :
      status.type === 'before' ? 'bg-blue-950/40 border-blue-700/50' :
      'bg-slate-800 border-slate-700'
    }`}>
      <div className="flex items-center justify-between">
        <h2 className="text-base font-semibold text-white">💼 勤務タイマー</h2>
        <span className={`text-xs px-2 py-1 rounded-full font-medium ${
          isOff ? 'bg-slate-700 text-slate-400' :
          status.type === 'before' ? 'bg-blue-600 text-white' :
          'bg-green-700 text-green-200'
        }`}>
          {isOff ? `${dayLabel}曜 公休日` : status.type === 'before' ? `${dayLabel}曜 勤務前` : `${dayLabel}曜 勤務中`}
        </span>
      </div>

      {isOff ? (
        <p className="text-slate-400 text-sm mt-3">お疲れ様です。今日は公休日です 🌙</p>
      ) : status.type === 'before' && status.remaining !== null ? (
        <div className="mt-3">
          <p className="text-slate-400 text-xs mb-1">9:00 勤務開始まで</p>
          <p className="text-3xl font-mono font-bold text-blue-400">{fmt(status.remaining)}</p>
        </div>
      ) : status.type === 'working' && status.remaining !== null ? (
        <div className="mt-3">
          <p className="text-slate-400 text-xs mb-1">勤務開始から</p>
          <p className="text-2xl font-mono font-bold text-green-400">{fmt(status.remaining)} 経過</p>
        </div>
      ) : null}
    </div>
  )
}
