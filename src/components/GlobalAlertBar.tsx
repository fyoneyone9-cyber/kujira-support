'use client'

import { useEffect, useRef, useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

type Counts = { critical: number; urgent: number; warning: number }

function daysLeftPaycube(endDate: string): number {
  const today = new Date()
  const end = new Date(endDate)
  return Math.ceil((end.getTime() - today.getTime()) / 86400000)
}

function daysLeftDelivery(dueDate: string): number {
  const today = new Date(); today.setHours(0, 0, 0, 0)
  const due = new Date(dueDate)
  return Math.ceil((due.getTime() - today.getTime()) / 86400000)
}

function playBeep(times: number) {
  try {
    const AudioCtx = window.AudioContext || (window as unknown as { webkitAudioContext: typeof AudioContext }).webkitAudioContext
    const ctx = new AudioCtx()
    for (let i = 0; i < times; i++) {
      const osc = ctx.createOscillator()
      const gain = ctx.createGain()
      osc.type = 'sine'
      osc.frequency.value = 880
      gain.gain.setValueAtTime(0.22, ctx.currentTime + i * 0.35)
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

const POLL_MS = 5 * 60 * 1000 // 5分おきに再チェック（ページ遷移してもバーは常駐なので定期更新する）

export default function GlobalAlertBar() {
  const pathname = usePathname()
  const [paycube, setPaycube] = useState<Counts>({ critical: 0, urgent: 0, warning: 0 })
  const [delivery, setDelivery] = useState<Counts & { overdue: number }>({ critical: 0, urgent: 0, warning: 0, overdue: 0 })
  const playedPaycube = useRef(false)
  const playedDelivery = useRef(false)

  const check = async () => {
    try {
      const r = await fetch('/api/paycube/contracts?mode=alert')
      const d = await r.json()
      let critical = 0, urgent = 0, warning = 0
      for (const c of (d.contracts || [])) {
        const days = daysLeftPaycube(c.end_date)
        if (days <= 14) critical++
        else if (days <= 30) urgent++
        else warning++
      }
      setPaycube({ critical, urgent, warning })
      if (!playedPaycube.current && critical > 0) {
        playedPaycube.current = true
        playBeep(2)
      }
    } catch { /* noop */ }

    try {
      const r = await fetch('/api/delivery/items?mode=alert')
      const d = await r.json()
      let critical = 0, urgent = 0, warning = 0, overdue = 0
      for (const it of (d.items || [])) {
        const days = daysLeftDelivery(it.delivery_due_date)
        if (days < 0) overdue++
        else if (days <= 3) critical++
        else if (days <= 7) urgent++
        else if (days <= 14) warning++
      }
      setDelivery({ critical, urgent, warning, overdue })
      if (!playedDelivery.current && (critical > 0 || overdue > 0)) {
        playedDelivery.current = true
        playBeep(overdue > 0 ? 3 : 2)
      }
    } catch { /* noop */ }
  }

  useEffect(() => {
    check()
    const timer = setInterval(check, POLL_MS)
    return () => clearInterval(timer)
  }, [])

  const paycubeTotal = paycube.critical + paycube.urgent + paycube.warning
  const deliveryTotal = delivery.critical + delivery.urgent + delivery.warning + delivery.overdue

  if (paycubeTotal === 0 && deliveryTotal === 0) return null

  const onPaycubePage = pathname === '/paycube'
  const onDeliveryPage = pathname === '/delivery'

  return (
    <div className="sticky top-0 z-40 flex flex-wrap gap-2 px-4 py-2 bg-slate-950 border-b border-slate-700">
      {paycubeTotal > 0 && !onPaycubePage && (
        <Link
          href="/paycube"
          className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-bold transition-colors
            ${paycube.critical > 0 ? 'bg-red-700 hover:bg-red-600 text-white animate-pulse'
              : paycube.urgent > 0 ? 'bg-orange-700 hover:bg-orange-600 text-white'
              : 'bg-yellow-700 hover:bg-yellow-600 text-white'}`}
        >
          <span>🔔</span>
          <span>PayCube保守</span>
          <span className="px-1.5 py-0.5 bg-black/30 rounded-full text-xs">{paycubeTotal}件</span>
        </Link>
      )}
      {deliveryTotal > 0 && !onDeliveryPage && (
        <Link
          href="/delivery"
          className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm font-bold transition-colors
            ${(delivery.overdue > 0 || delivery.critical > 0) ? 'bg-red-700 hover:bg-red-600 text-white animate-pulse'
              : delivery.urgent > 0 ? 'bg-orange-700 hover:bg-orange-600 text-white'
              : 'bg-yellow-700 hover:bg-yellow-600 text-white'}`}
        >
          <span>📦</span>
          <span>IoT製品納品アラート</span>
          <span className="px-1.5 py-0.5 bg-black/30 rounded-full text-xs">{deliveryTotal}件</span>
        </Link>
      )}
    </div>
  )
}
