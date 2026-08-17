'use client'

import { useEffect, useState } from 'react'
import Link from 'next/link'

type AlertSummary = {
  critical: number
  urgent: number
  warning: number
}

export default function PayCubeAlertBanner() {
  const [summary, setSummary] = useState<AlertSummary | null>(null)

  useEffect(() => {
    fetch('/api/paycube/contracts?mode=alert')
      .then(r => r.json())
      .then(d => {
        const today = new Date()
        const twoWeeks = new Date(today); twoWeeks.setDate(today.getDate() + 14)
        const oneMonth = new Date(today); oneMonth.setMonth(today.getMonth() + 1)
        let critical = 0, urgent = 0, warning = 0
        for (const c of (d.contracts || [])) {
          const end = new Date(c.end_date)
          if (end <= twoWeeks) critical++
          else if (end <= oneMonth) urgent++
          else warning++
        }
        setSummary({ critical, urgent, warning })
      })
      .catch(() => {})
  }, [])

  if (!summary || (summary.critical + summary.urgent + summary.warning) === 0) return null

  return (
    <Link href="/paycube">
      <div className={`mb-6 flex items-center gap-4 px-5 py-4 rounded-xl border cursor-pointer transition-opacity hover:opacity-90
        ${summary.critical > 0
          ? 'bg-red-950/70 border-red-500 animate-pulse'
          : summary.urgent > 0
          ? 'bg-orange-950/60 border-orange-500'
          : 'bg-yellow-950/40 border-yellow-600'}`}>
        <span className="text-3xl">{summary.critical > 0 ? '🚨' : summary.urgent > 0 ? '⚠️' : '📋'}</span>
        <div className="flex-1">
          <p className={`font-bold text-base ${summary.critical > 0 ? 'text-red-200' : summary.urgent > 0 ? 'text-orange-200' : 'text-yellow-200'}`}>
            PayCube保守期限アラート
          </p>
          <p className="text-sm text-slate-300 mt-0.5">
            {summary.critical > 0 && <span className="text-red-300 font-medium">🔴 緊急{summary.critical}件　</span>}
            {summary.urgent > 0 && <span className="text-orange-300 font-medium">🟠 要対応{summary.urgent}件　</span>}
            {summary.warning > 0 && <span className="text-yellow-300 font-medium">🟡 注意{summary.warning}件　</span>}
          </p>
        </div>
        <span className="text-slate-400 text-sm">詳細 →</span>
      </div>
    </Link>
  )
}
