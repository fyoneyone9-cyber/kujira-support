'use client'

import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'

type DeliveryItem = {
  id: string
  client_name: string
  product_name: string
  delivery_due_date: string
  status: string
}

type Summary = {
  critical: number  // 3日以内
  urgent: number    // 7日以内
  warning: number   // 14日以内
  overdue: number   // 納品予定日を過ぎている
}

function daysLeft(dueDate: string): number {
  const today = new Date(); today.setHours(0, 0, 0, 0)
  const due = new Date(dueDate)
  return Math.ceil((due.getTime() - today.getTime()) / 86400000)
}

// Web Audio APIでビープ音を鳴らす（音声ファイル不要）
function playBeep(times: number) {
  try {
    const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext
    const ctx = new AudioCtx()
    for (let i = 0; i < times; i++) {
      const osc = ctx.createOscillator()
      const gain = ctx.createGain()
      osc.type = 'sine'
      osc.frequency.value = 880
      gain.gain.setValueAtTime(0.25, ctx.currentTime + i * 0.35)
      gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + i * 0.35 + 0.3)
      osc.connect(gain)
      gain.connect(ctx.destination)
      osc.start(ctx.currentTime + i * 0.35)
      osc.stop(ctx.currentTime + i * 0.35 + 0.3)
    }
  } catch {
    // Audio未対応環境では無視
  }
}

export default function DeliveryAlertBanner() {
  const [summary, setSummary] = useState<Summary | null>(null)
  const [nearest, setNearest] = useState<DeliveryItem | null>(null)
  const played = useRef(false)

  useEffect(() => {
    fetch('/api/delivery/items?mode=alert')
      .then(r => r.json())
      .then(d => {
        const items: DeliveryItem[] = d.items || []
        let critical = 0, urgent = 0, warning = 0, overdue = 0
        let nearestItem: DeliveryItem | null = null
        let nearestDays = Infinity
        for (const it of items) {
          const days = daysLeft(it.delivery_due_date)
          if (days < 0) overdue++
          else if (days <= 3) critical++
          else if (days <= 7) urgent++
          else if (days <= 14) warning++
          if (days < nearestDays) { nearestDays = days; nearestItem = it }
        }
        setSummary({ critical, urgent, warning, overdue })
        setNearest(nearestItem)

        // 緊急(3日以内)または期限超過がある場合、ページ読み込み時に一度だけ音を鳴らす
        if (!played.current && (critical > 0 || overdue > 0)) {
          played.current = true
          playBeep(overdue > 0 ? 3 : 2)
        }
      })
      .catch(() => {})
  }, [])

  if (!summary || (summary.critical + summary.urgent + summary.warning + summary.overdue) === 0) return null

  const level = summary.overdue > 0 ? 'overdue' : summary.critical > 0 ? 'critical' : summary.urgent > 0 ? 'urgent' : 'warning'

  const style = {
    overdue:  { bg: 'bg-red-950/80 border-red-400 animate-pulse', text: 'text-red-200', icon: '🚨' },
    critical: { bg: 'bg-red-950/70 border-red-500 animate-pulse', text: 'text-red-200', icon: '🚨' },
    urgent:   { bg: 'bg-orange-950/60 border-orange-500', text: 'text-orange-200', icon: '⚠️' },
    warning:  { bg: 'bg-yellow-950/40 border-yellow-600', text: 'text-yellow-200', icon: '📦' },
  }[level]

  return (
    <Link href="/delivery">
      <div className={`mb-6 flex items-center gap-4 px-5 py-4 rounded-xl border cursor-pointer transition-opacity hover:opacity-90 ${style.bg}`}>
        <span className="text-3xl">{style.icon}</span>
        <div className="flex-1">
          <p className={`font-bold text-base ${style.text}`}>
            IoT製品 納品予定日アラート
          </p>
          <p className="text-sm text-slate-300 mt-0.5">
            {summary.overdue > 0 && <span className="text-red-300 font-bold">🔴 期限超過{summary.overdue}件　</span>}
            {summary.critical > 0 && <span className="text-red-300 font-medium">🔴 3日以内{summary.critical}件　</span>}
            {summary.urgent > 0 && <span className="text-orange-300 font-medium">🟠 1週間以内{summary.urgent}件　</span>}
            {summary.warning > 0 && <span className="text-yellow-300 font-medium">🟡 2週間以内{summary.warning}件　</span>}
          </p>
          {nearest && (
            <p className="text-xs text-slate-400 mt-1">
              直近: {nearest.client_name} / {nearest.product_name}（{nearest.delivery_due_date}）
            </p>
          )}
        </div>
        <span className="text-slate-400 text-sm">詳細 →</span>
      </div>
    </Link>
  )
}
