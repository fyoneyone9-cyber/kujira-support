'use client'

import { useEffect, useState } from 'react'

type DeliveryItem = {
  id: string
  client_name: string
  install_address: string
  product_name: string
  quantity: number | null
  progress: string
  assignee: string
  delivery_due_date: string
  delivery_date: string | null
  contact_name: string
  contact_tel1: string
  contact_tel2: string
  notes: string
  status: string
  created_at: string
}

type AlertLevel = 'overdue' | 'critical' | 'urgent' | 'warning' | 'ok'

function daysLeft(dueDate: string): number {
  const today = new Date(); today.setHours(0, 0, 0, 0)
  const due = new Date(dueDate)
  return Math.ceil((due.getTime() - today.getTime()) / 86400000)
}

function getAlertLevel(dueDate: string): AlertLevel {
  const days = daysLeft(dueDate)
  if (days < 0) return 'overdue'
  if (days <= 3) return 'critical'
  if (days <= 7) return 'urgent'
  if (days <= 14) return 'warning'
  return 'ok'
}

const levelStyle: Record<AlertLevel, { bg: string; border: string; badge: string; label: string; icon: string }> = {
  overdue:  { bg: 'bg-red-950/70', border: 'border-red-400', badge: 'bg-red-700 text-white', label: '🔴 期限超過', icon: '🚨' },
  critical: { bg: 'bg-red-950/60', border: 'border-red-500', badge: 'bg-red-600 text-white', label: '🔴 3日以内', icon: '🚨' },
  urgent:   { bg: 'bg-orange-950/60', border: 'border-orange-500', badge: 'bg-orange-500 text-white', label: '🟠 1週間以内', icon: '⚠️' },
  warning:  { bg: 'bg-yellow-950/60', border: 'border-yellow-500', badge: 'bg-yellow-600 text-white', label: '🟡 2週間以内', icon: '📦' },
  ok:       { bg: 'bg-slate-800', border: 'border-slate-700', badge: 'bg-slate-600 text-slate-200', label: '✅ 余裕あり', icon: '✅' },
}

export default function DeliveryPage() {
  const [items, setItems] = useState<DeliveryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'alert' | 'all' | 'done'>('alert')
  const [updating, setUpdating] = useState<string | null>(null)
  const [importing, setImporting] = useState(false)
  const [importResult, setImportResult] = useState<string | null>(null)
  const [stats, setStats] = useState<{ total: number; lastImport: string | null } | null>(null)

  const load = async () => {
    setLoading(true)
    const mode = filter === 'alert' ? '?mode=alert' : ''
    const res = await fetch(`/api/delivery/items${mode}`)
    const d = await res.json()
    let data: DeliveryItem[] = d.items || []
    if (filter === 'done') data = data.filter(i => i.status === 'done')
    setItems(data.sort((a, b) => a.delivery_due_date.localeCompare(b.delivery_due_date)))
    setLoading(false)
  }

  const loadStats = async () => {
    const res = await fetch('/api/delivery/items')
    const d = await res.json()
    const all: DeliveryItem[] = d.items || []
    const lastImport = all.length > 0
      ? all.reduce((a, b) => a.created_at > b.created_at ? a : b).created_at
      : null
    setStats({ total: all.length, lastImport })
  }

  useEffect(() => { load() }, [filter])
  useEffect(() => { loadStats() }, [])

  const markDone = async (id: string) => {
    setUpdating(id)
    await fetch('/api/delivery/items', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, status: 'done', acknowledged_at: new Date().toISOString() })
    })
    setUpdating(null)
    load()
  }

  const overdue  = items.filter(i => getAlertLevel(i.delivery_due_date) === 'overdue')
  const critical = items.filter(i => getAlertLevel(i.delivery_due_date) === 'critical')
  const urgent   = items.filter(i => getAlertLevel(i.delivery_due_date) === 'urgent')

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">📦 IoT製品 納品予定アラート</h1>
        <p className="text-slate-400 text-base mt-1">納品予定日が近いものから自動で上位表示されます。「【管理】IoT製品納品一覧」のCSVを取り込んでください。</p>
      </div>

      {/* データステータスバー */}
      <div className="flex flex-wrap gap-3 mb-4 text-sm">
        <div className="flex items-center gap-2 px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg">
          <span className="text-slate-400">📦 登録件数</span>
          <span className="font-bold text-white">{stats ? `${stats.total}件` : '...'}</span>
        </div>
        <div className="flex items-center gap-2 px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg">
          <span className="text-slate-400">🕐 最終取込</span>
          <span className="font-bold text-white">
            {stats?.lastImport
              ? new Date(stats.lastImport).toLocaleString('ja-JP', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
              : '...'}
          </span>
        </div>
      </div>

      {/* アラートサマリーバナー */}
      {(overdue.length > 0 || critical.length > 0 || urgent.length > 0) && filter === 'alert' && (
        <div className="mb-6 space-y-3">
          {overdue.length > 0 && (
            <div className="flex items-center gap-3 px-5 py-4 bg-red-950/80 border border-red-400 rounded-xl animate-pulse">
              <span className="text-2xl">🚨</span>
              <div>
                <p className="font-bold text-red-200 text-lg">期限超過！{overdue.length}件が納品予定日を過ぎています</p>
                <p className="text-red-300 text-sm">至急状況を確認してください</p>
              </div>
            </div>
          )}
          {critical.length > 0 && (
            <div className="flex items-center gap-3 px-5 py-4 bg-red-900/80 border border-red-500 rounded-xl animate-pulse">
              <span className="text-2xl">🚨</span>
              <div>
                <p className="font-bold text-red-200 text-lg">緊急！{critical.length}件が3日以内に納品予定</p>
              </div>
            </div>
          )}
          {urgent.length > 0 && (
            <div className="flex items-center gap-3 px-5 py-4 bg-orange-900/60 border border-orange-500 rounded-xl">
              <span className="text-2xl">⚠️</span>
              <div>
                <p className="font-bold text-orange-200">{urgent.length}件が1週間以内に納品予定</p>
              </div>
            </div>
          )}
        </div>
      )}

      {/* コントロール */}
      <div className="flex gap-3 mb-5 flex-wrap">
        <button
          onClick={() => setFilter('alert')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'alert' ? 'bg-red-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}
        >
          🔔 未納品のみ
        </button>
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'all' ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}
        >
          📋 全件表示
        </button>
        <button
          onClick={() => setFilter('done')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'done' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}
        >
          ✅ 納品完了分
        </button>
        <label className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors cursor-pointer ml-auto ${importing ? 'bg-slate-600 text-slate-400' : 'bg-purple-700 hover:bg-purple-600 text-white'}`}>
          {importing ? '⏳ 取込中...' : '📥 CSVで一括更新'}
          <input
            type="file"
            accept=".csv"
            className="hidden"
            disabled={importing}
            onChange={async (e) => {
              const file = e.target.files?.[0]
              if (!file) return
              setImporting(true)
              setImportResult(null)
              const fd = new FormData()
              fd.append('file', file)
              const res = await fetch('/api/delivery/import-csv', { method: 'POST', body: fd })
              const d = await res.json()
              if (d.ok) {
                setImportResult(`✅ 取込完了：${d.imported}件`)
                loadStats()
                load()
              } else {
                setImportResult(`❌ エラー：${d.error}`)
              }
              setImporting(false)
              e.target.value = ''
            }}
          />
        </label>
      </div>

      {importResult && (
        <div className={`mb-3 px-4 py-3 rounded-lg text-sm font-medium ${importResult.startsWith('✅') ? 'bg-green-900/60 border border-green-600 text-green-200' : 'bg-red-900/60 border border-red-600 text-red-200'}`}>
          {importResult}
          <span className="ml-2 text-xs text-slate-400">スプレッドシートをCSVでダウンロード → このボタンで再取込すれば常に最新状態になります</span>
        </div>
      )}

      {/* 一覧 */}
      {loading ? (
        <div className="text-slate-400 text-center py-12">読み込み中...</div>
      ) : items.length === 0 ? (
        <div className="text-slate-400 text-center py-12">
          <p className="text-4xl mb-3">✅</p>
          <p>対象の案件はありません</p>
        </div>
      ) : (
        <div className="space-y-3">
          {items.map(it => {
            const level = getAlertLevel(it.delivery_due_date)
            const s = levelStyle[level]
            const days = daysLeft(it.delivery_due_date)
            return (
              <div key={it.id} className={`${s.bg} border ${s.border} rounded-xl p-4`}>
                <div className="flex items-start justify-between gap-3 flex-wrap">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap mb-1">
                      <span className="text-lg">{s.icon}</span>
                      <span className="font-bold text-white text-base">{it.client_name}</span>
                      {it.status !== 'done' && <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${s.badge}`}>{s.label}</span>}
                      {it.status === 'done' && <span className="text-xs px-2 py-0.5 rounded-full bg-green-700 text-white font-medium">✅ 納品完了</span>}
                      {it.progress && <span className="text-xs px-2 py-0.5 rounded-full bg-slate-600 text-slate-200">{it.progress}</span>}
                    </div>
                    <div className="text-base text-slate-300 space-y-1">
                      <p>📅 納品予定日: <span className={`font-bold ${level === 'overdue' || level === 'critical' ? 'text-red-300' : level === 'urgent' ? 'text-orange-300' : level === 'warning' ? 'text-yellow-300' : 'text-white'}`}>{it.delivery_due_date}</span>
                        {it.status !== 'done' && <span className="text-slate-400"> （{days < 0 ? `${-days}日超過` : `残 ${days}日`}）</span>}
                      </p>
                      {it.product_name && <p>📦 製品: {it.product_name}{it.quantity ? ` × ${it.quantity}` : ''}</p>}
                      {it.install_address && <p className="text-slate-400 text-sm">📍 {it.install_address}</p>}
                      {it.assignee && <p>👤 担当: {it.assignee}</p>}
                      {(it.contact_name || it.contact_tel1) && <p>☎️ {it.contact_name} {it.contact_tel1}</p>}
                      {it.notes && <p className="text-slate-400">📝 {it.notes}</p>}
                    </div>
                  </div>
                  {it.status !== 'done' && (
                    <div className="flex flex-col gap-2 min-w-fit">
                      <button
                        disabled={updating === it.id}
                        onClick={() => markDone(it.id)}
                        className="px-4 py-2 bg-green-700 hover:bg-green-600 text-white text-sm rounded-lg font-medium transition-colors whitespace-nowrap"
                      >
                        ✅ 納品完了にする
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
