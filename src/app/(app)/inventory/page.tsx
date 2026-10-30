'use client'

export const dynamic = 'force-dynamic'

import { useEffect, useState } from 'react'

type InvItem = {
  id: string
  part_no: string | null
  product_name: string
  stock: number
  incoming: number
  required: number
  diff: number
  notes: string | null
  last_stocktake_date: string | null
  missing_in_last_import: boolean | null
  acknowledged_at: string | null
  imported_at: string | null
}

const LOW_THRESHOLD = 3 // 残りわずか（これ以下で念のためアラート）

type Level = 'out' | 'low' | 'soon' | 'ok'
function itemLevel(it: InvItem): Level {
  // 在庫切れ: 在庫0以下 または 差分マイナス（必要数に足りない）
  if (it.stock <= 0 || it.diff < 0) return 'out'
  // 残りわずか
  if (it.stock <= LOW_THRESHOLD) return 'low'
  // もうすぐ必要数割れ（在庫 - 必要数 が小さい）
  if (it.required > 0 && (it.stock - it.required) <= LOW_THRESHOLD) return 'soon'
  return 'ok'
}
const levelStyle: Record<Level, { bg: string; border: string; badge: string; label: string; icon: string }> = {
  out:  { bg: 'bg-red-950/60',    border: 'border-red-500',    badge: 'bg-red-600 text-white',      label: '在庫切れ/不足', icon: '🚨' },
  low:  { bg: 'bg-orange-950/50', border: 'border-orange-500', badge: 'bg-orange-500 text-white',   label: '残りわずか',    icon: '⚠️' },
  soon: { bg: 'bg-yellow-950/40', border: 'border-yellow-600', badge: 'bg-yellow-600 text-white',   label: '要注意',        icon: '📦' },
  ok:   { bg: 'bg-slate-800',     border: 'border-slate-700',  badge: 'bg-slate-600 text-slate-200', label: '十分',          icon: '✅' },
}

export default function InventoryPage() {
  const [items, setItems] = useState<InvItem[]>([])
  const [loading, setLoading] = useState(true)
  const [importing, setImporting] = useState(false)
  const [msg, setMsg] = useState('')
  const [csvQueue, setCsvQueue] = useState<File[]>([])

  const load = async () => {
    setLoading(true)
    const res = await fetch('/api/inventory/items', { cache: 'no-store' })
    const d = await res.json()
    setItems((d.items || []) as InvItem[])
    setLoading(false)
  }
  useEffect(() => { load() }, [])

  const importOne = async (file: File) => {
    const fd = new FormData(); fd.append('file', file)
    const res = await fetch('/api/inventory/import-csv', { method: 'POST', body: fd })
    const j = await res.json()
    if (!res.ok || j.error) throw new Error(j.error || String(res.status))
    return j as { inserted: number; updated: number; missing: number }
  }
  // キューに溜めたCSVをまとめて取込実行
  const runQueue = async () => {
    if (csvQueue.length === 0) { setMsg('取込するCSVがありません。「＋CSV追加」で選んでください。'); return }
    setImporting(true)
    let ins = 0, upd = 0, mis = 0, ok = 0
    for (let i = 0; i < csvQueue.length; i++) {
      setMsg(`取込中… (${i + 1}/${csvQueue.length}) ${csvQueue[i].name}`)
      try { const r = await importOne(csvQueue[i]); ins += r.inserted; upd += r.updated; mis = r.missing; ok++ }
      catch (e) { setMsg('❌ ' + csvQueue[i].name + ': ' + (e as Error).message) }
    }
    setMsg(`✅ 取込完了: ${ok}ファイル / 新規${ins} 更新${upd} 今回なし${mis}`)
    setCsvQueue([])
    await load()
    setImporting(false)
  }

  // 最終インポートからの経過時間（24h判定）
  const lastImport = items.reduce<string | null>((a, it) => {
    if (!it.imported_at) return a
    return !a || it.imported_at > a ? it.imported_at : a
  }, null)
  const hoursSinceImport = lastImport ? (Date.now() - new Date(lastImport).getTime()) / 3600000 : null
  const stale = hoursSinceImport !== null && hoursSinceImport > 24

  const outItems = items.filter(it => itemLevel(it) === 'out' && !it.missing_in_last_import)
  const lowItems = items.filter(it => itemLevel(it) === 'low' && !it.missing_in_last_import)
  const sorted = [...items].sort((a, b) => {
    const order: Level[] = ['out', 'low', 'soon', 'ok']
    return order.indexOf(itemLevel(a)) - order.indexOf(itemLevel(b)) || a.product_name.localeCompare(b.product_name)
  })

  const patch = async (id: string, updates: Record<string, unknown>) => {
    setItems(prev => prev.map(it => it.id === id ? { ...it, ...updates } : it))
    await fetch('/api/inventory/items', { method: 'PATCH', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id, ...updates }) })
  }

  return (
    <div className="p-4 md:p-6 space-y-4 max-w-5xl mx-auto">
      <div className="flex items-center gap-3 flex-wrap">
        <h1 className="text-xl font-bold text-white">📦 在庫管理</h1>
        <label className="px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-slate-200 text-sm font-bold rounded-lg cursor-pointer">
          ＋CSV追加
          <input type="file" accept=".csv" multiple className="hidden" disabled={importing}
            onChange={e => { const fs = Array.from(e.target.files || []); if (fs.length) setCsvQueue(q => [...q, ...fs]); e.currentTarget.value = '' }} />
        </label>
        <button onClick={runQueue} disabled={importing || csvQueue.length === 0}
          className={`px-3 py-1.5 text-sm font-bold rounded-lg ${importing || csvQueue.length === 0 ? 'bg-slate-700 text-slate-500 cursor-not-allowed' : 'bg-emerald-700 hover:bg-emerald-600 text-white'}`}>
          {importing ? '⏳ 取込中…' : `📥 取込実行${csvQueue.length > 0 ? `（${csvQueue.length}件）` : ''}`}
        </button>
        {/* キュー表示 */}
        {csvQueue.length > 0 && (
          <div className="flex items-center gap-1.5 flex-wrap">
            {csvQueue.map((f, i) => (
              <span key={i} className="flex items-center gap-1 px-2 py-1 bg-slate-700 rounded text-xs text-slate-200">
                📄{f.name}
                <button onClick={() => setCsvQueue(q => q.filter((_, j) => j !== i))} className="text-slate-400 hover:text-red-400 ml-1">✕</button>
              </span>
            ))}
          </div>
        )}
        {msg && <span className="text-sm text-slate-300">{msg}</span>}
      </div>

      {/* 24時間アラート */}
      {stale && (
        <div className="bg-red-950/70 border border-red-500 rounded-lg px-4 py-3 text-red-200 font-bold animate-pulse">
          🕐 在庫データが {Math.floor(hoursSinceImport!)} 時間前から更新されていません（24時間以内にインポートしてください）
        </div>
      )}
      {lastImport && !stale && (
        <p className="text-xs text-slate-500">最終インポート: {new Date(lastImport).toLocaleString('ja-JP')}（{Math.floor(hoursSinceImport!)}時間前）</p>
      )}
      {!lastImport && !loading && (
        <div className="bg-slate-800 border border-slate-600 rounded-lg px-4 py-3 text-slate-300">在庫データがありません。CSVをインポートしてください。</div>
      )}

      {/* 在庫切れサマリ */}
      {(outItems.length > 0 || lowItems.length > 0) && (
        <div className="bg-red-950/40 border border-red-700 rounded-lg px-4 py-3 space-y-1">
          {outItems.length > 0 && <p className="text-red-300 font-bold">🚨 在庫切れ/不足: {outItems.length}品目 — {outItems.map(i => i.product_name).slice(0, 8).join('・')}{outItems.length > 8 ? ' …' : ''}</p>}
          {lowItems.length > 0 && <p className="text-orange-300 font-bold">⚠️ 残りわずか({LOW_THRESHOLD}以下): {lowItems.length}品目 — {lowItems.map(i => i.product_name).slice(0, 8).join('・')}{lowItems.length > 8 ? ' …' : ''}</p>}
        </div>
      )}

      {/* 品目一覧 */}
      <div className="space-y-2">
        {sorted.map(it => {
          const lv = itemLevel(it); const s = levelStyle[lv]
          return (
            <div key={it.id} className={`${s.bg} border ${s.border} rounded-xl p-3 flex items-center gap-3 flex-wrap ${it.missing_in_last_import ? 'opacity-50' : ''}`}>
              <span className="text-lg">{s.icon}</span>
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="font-bold text-white">{it.product_name}</span>
                  {it.part_no && <span className="text-xs text-slate-500 font-mono">{it.part_no}</span>}
                  <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${s.badge}`}>{s.label}</span>
                  {it.missing_in_last_import && <span className="text-xs px-2 py-0.5 rounded-full bg-slate-700 text-slate-400">前回取込なし</span>}
                </div>
                {it.notes && <p className="text-xs text-slate-400 mt-0.5">{it.notes}</p>}
              </div>
              <div className="flex items-center gap-4 text-sm">
                <span className="text-slate-300">在庫 <b className={it.stock <= 0 ? 'text-red-400' : it.stock <= LOW_THRESHOLD ? 'text-orange-400' : 'text-white'}>{it.stock}</b></span>
                <span className="text-slate-500">入荷予定 {it.incoming}</span>
                <span className="text-slate-500">必要 {it.required}</span>
                <span className={`font-bold ${it.diff < 0 ? 'text-red-400' : 'text-slate-400'}`}>差分 {it.diff}</span>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
