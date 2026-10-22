'use client'

import { useEffect, useState } from 'react'

type Equipment = { name?: string; value?: string }

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
  dashboard_memo?: string | null
  dashboard_todos?: Record<string, unknown> | null
  worker_needed?: boolean | null
  worker_contacts?: { name?: string; tel?: string; email?: string }[] | null
  work_date?: string | null
  jitbox_ordered?: boolean | null
  p400_mtid?: string | null
  p400_tid?: string | null
  locked?: boolean | null
  p400_status?: string | null
  paycube_status?: string | null
  vega3000_status?: string | null
  equipment?: Equipment[] | null
  item_key?: string | null
  slack_url?: string | null
  hubspot_url?: string | null
  process_sheet_url?: string | null
  hearing_sheet_url?: string | null
  payment_received?: boolean | null
  missing_in_last_import?: boolean | null
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
  overdue:  { bg: 'bg-red-950/70',    border: 'border-red-400',    badge: 'bg-red-700 text-white',       label: '期限超過', icon: '🚨' },
  critical: { bg: 'bg-red-950/60',    border: 'border-red-500',    badge: 'bg-red-600 text-white',       label: '3日以内',  icon: '🚨' },
  urgent:   { bg: 'bg-orange-950/60', border: 'border-orange-500', badge: 'bg-orange-500 text-white',    label: '1週間以内', icon: '⚠️' },
  warning:  { bg: 'bg-yellow-950/60', border: 'border-yellow-500', badge: 'bg-yellow-600 text-white',    label: '2週間以内', icon: '📦' },
  ok:       { bg: 'bg-slate-800',     border: 'border-slate-700',  badge: 'bg-slate-600 text-slate-200', label: '余裕あり',  icon: '✅' },
}

// 設置先住所からJITボックスのリードタイムを判定（大阪発）
function jitLeadDays(address: string): number {
  if (/北海道|沖縄|離島/.test(address)) return 3
  return 2
}

// P400/PayCube=60日（2か月）、PayPay=10日、Vega3000=14日
const LEAD_TIME: Record<string, number> = { 'P400': 60, 'PayCube': 60, 'PayPay': 60 }
const EQUIP_STATUSES = ['未発注', '発注済み', '入荷履歴', '発送済み', '納品完了', '設定完了']

type TodoItem = { label: string; deadlineDate: string | null; urgent: boolean }

// 日付に日数を加算してYYYY-MM-DD返却
function addDays(dateStr: string, days: number): string {
  const d = new Date(dateStr)
  d.setDate(d.getDate() + days)
  return d.toISOString().slice(0, 10)
}

function buildTodoItems(
  equipment: Equipment[] | null | undefined,
  workerNeeded: boolean | null | undefined,
  dueDate: string,
  jitDays: number,
  workDate: string | null | undefined,
  paymentReceived: boolean | null | undefined
): TodoItem[] {
  const eq = equipment || []
  const today = new Date(); today.setHours(0,0,0,0)
  const makeItem = (label: string, deadlineDaysBeforeDue: number | null): TodoItem => {
    const deadlineDate = deadlineDaysBeforeDue !== null ? addDays(dueDate, -deadlineDaysBeforeDue) : null
    const urgent = deadlineDate ? (new Date(deadlineDate).getTime() - today.getTime()) / 86400000 <= 3 : false
    return { label, deadlineDate, urgent }
  }
  const todos: TodoItem[] = []
  if (eq.find(e => e.name === 'P400'))     todos.push(makeItem('P400 手配', 60))
  if (eq.find(e => e.name === 'PayCube')) {
    if (paymentReceived) {
      todos.push(makeItem('PayCube 手配', 60))
    } else {
      todos.push({ label: 'PayCube 手配（入金待ち）', deadlineDate: null, urgent: false })
    }
  }
  if (eq.find(e => e.name === 'PayPay'))   todos.push(makeItem('PayPay 手配', 60))
  todos.push(makeItem('JITボックス 発注', jitDays))
  if (workerNeeded) {
    const baseDate = workDate ? workDate : dueDate
    const wDeadline = addDays(baseDate, -21)
    const wDays = Math.ceil((new Date(wDeadline).getTime() - today.getTime()) / 86400000)
    todos.push({ label: '作業員 手配', deadlineDate: wDeadline, urgent: wDays <= 3 })
  }
  todos.push(makeItem('出荷 手配', jitDays))
  todos.push(makeItem('施工日 確定', 14))
  return todos
}

// 機材デート管理コンポーネント（発注日・到着予定日・実到着日）
type EquipDateProps = {
  name: string
  todos: Record<string, unknown> | null | undefined
  onSave: (key: string, val: string) => void
  dueDate: string
}
function EquipDates({ name, todos, onSave, dueDate }: EquipDateProps) {
  const prefix = name.toLowerCase().replace(/[^a-z0-9]/g, '')
  const orderKey   = `${prefix}_order_date`
  const arriveKey  = `${prefix}_arrive_date`
  const actualKey  = `${prefix}_actual_date`
  const lt = LEAD_TIME[name] || 0
  const orderDate  = (todos?.[orderKey]  as string) || ''
  const arriveDate = (todos?.[arriveKey] as string) || ''
  const actualDate = (todos?.[actualKey] as string) || ''

  // 発注日から到着予定日を自動計算
  const calcArrive = (od: string) => {
    if (!od || !lt) return ''
    const d = new Date(od)
    d.setDate(d.getDate() + lt)
    return d.toISOString().slice(0, 10)
  }

  // 到着予定日 vs 納品予定日
  const expectedArrive = arriveDate || calcArrive(orderDate)
  const arriveVsDue = expectedArrive && dueDate ? daysLeft(dueDate) - daysLeft(expectedArrive) : null

  return (
    <div className="mt-2 bg-slate-900/40 rounded-lg px-3 py-2 space-y-1.5">
      <div className="flex items-center gap-2 text-xs">
        <span className="text-slate-500 w-20">発注日:</span>
        <input type="date" defaultValue={orderDate}
          onBlur={e => {
            onSave(orderKey, e.target.value)
            if (e.target.value && !arriveDate) onSave(arriveKey, calcArrive(e.target.value))
          }}
          className="px-1.5 py-0.5 bg-slate-800 border border-slate-600 rounded text-white text-xs"
        />
      </div>
      <div className="flex items-center gap-2 text-xs">
        <span className="text-slate-500 w-20">到着予定:</span>
        <input type="date" defaultValue={arriveDate || calcArrive(orderDate)}
          onBlur={e => onSave(arriveKey, e.target.value)}
          className="px-1.5 py-0.5 bg-slate-800 border border-slate-600 rounded text-white text-xs"
        />
        {arriveVsDue !== null && (
          <span className={`text-xs font-bold ${arriveVsDue < 0 ? 'text-red-400 animate-pulse' : arriveVsDue < 7 ? 'text-orange-400' : 'text-green-400'}`}>
            {arriveVsDue < 0 ? `納品日${-arriveVsDue}日后到着→間に合わない！` : `納品日まで${arriveVsDue}日前到着`}
          </span>
        )}
      </div>
      <div className="flex items-center gap-2 text-xs">
        <span className="text-slate-500 w-20">実到着日:</span>
        <input type="date" defaultValue={actualDate}
          onBlur={e => onSave(actualKey, e.target.value)}
          className="px-1.5 py-0.5 bg-slate-800 border border-slate-600 rounded text-white text-xs"
        />
        {actualDate && <span className="text-green-400 text-xs">入荷確認済</span>}
      </div>
      {lt > 0 && <p className="text-slate-600 text-xs">リードタイム目安: {lt}日</p>}
    </div>
  )
}

type PaymentSectionProps = {
  it: DeliveryItem
  patch: (id: string, u: Record<string, unknown>) => void
  saveTodoKey: (id: string, todos: Record<string, unknown> | null | undefined, key: string, val: string) => void
}
function PaymentSection({ it, patch, saveTodoKey }: PaymentSectionProps) {
  const [open, setOpen] = useState(false)
  const payStatus = (it.dashboard_todos?.['payment_status'] as string) || '請求未発行'
  const badgeColor = payStatus === '入金不要（無償）' ? 'bg-slate-600 text-slate-300' :
    payStatus === '入金確認済み' ? 'bg-green-800 text-green-200' :
    payStatus === '入金超過・要確認' ? 'bg-red-800 text-red-200 animate-pulse' :
    payStatus === '入金待ち' ? 'bg-yellow-800 text-yellow-200' :
    payStatus === '見積書作成中（確認中）' ? 'bg-indigo-800 text-indigo-200' :
    payStatus === '見積書送付済み' ? 'bg-teal-800 text-teal-200' :
    payStatus === '請求書発行済' ? 'bg-blue-800 text-blue-200' :
    'bg-slate-700 text-slate-400'
  return (
    <div className="border-t border-slate-700/50 pt-3 space-y-3">
      <button onClick={() => setOpen(v => !v)} className="flex items-center gap-2 w-full text-left">
        <span className="text-slate-400 font-bold text-sm">入金管理</span>
        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${badgeColor}`}>{payStatus}</span>
        <span className="ml-auto text-slate-500 text-xs">{open ? '▲ 閉じる' : '▼ 開く'}</span>
      </button>
      {open && (
        <div className="space-y-3">
          <div className="flex flex-wrap gap-1.5">
            {['入金不要（無償）', '請求未発行', '見積書作成中（確認中）', '見積書送付済み', '請求書発行済', '入金待ち', '入金確認済み', '入金超過・要確認'].map(st => {
              const isActive = payStatus === st
              const isDone = st === '入金確認済み'
              const isAlert = st === '入金超過・要確認'
              return (
                <button key={st}
                  onClick={() => {
                    saveTodoKey(it.id, it.dashboard_todos, 'payment_status', st)
                    if (isDone || st === '入金不要（無償）') patch(it.id, { payment_received: true })
                    else if (isActive) patch(it.id, { payment_received: false })
                  }}
                  className={`px-3 py-1 text-xs rounded-lg font-medium transition-colors ${
                    isActive && isDone ? 'bg-green-700 text-white' :
                    isActive && isAlert ? 'bg-red-700 text-white animate-pulse' :
                    isActive ? 'bg-blue-600 text-white' :
                    'bg-slate-700 text-slate-300 hover:bg-slate-500'
                  }`}>{st}</button>
              )
            })}
          </div>
          {!it.payment_received && payStatus !== '入金不要（無償）' && (it.equipment || []).some((e: {name?: string}) => e.name === 'PayCube') && <p className="text-xs text-orange-400 font-bold">⚠️ PayCubeは入金確認後に発注</p>}
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500 w-28">請求書発行日:</span>
            <input type="date" defaultValue={(it.dashboard_todos?.['invoice_date'] as string) || ''}
              onBlur={(e) => saveTodoKey(it.id, it.dashboard_todos, 'invoice_date', e.target.value)}
              className="px-2 py-0.5 text-xs bg-slate-800 border border-slate-600 rounded text-white" />
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500 w-28">入金期限日:</span>
            <input type="date" defaultValue={(it.dashboard_todos?.['payment_due_date'] as string) || ''}
              onBlur={(e) => saveTodoKey(it.id, it.dashboard_todos, 'payment_due_date', e.target.value)}
              className="px-2 py-0.5 text-xs bg-slate-800 border border-slate-600 rounded text-white" />
            {(() => {
              const pd = it.dashboard_todos?.['payment_due_date'] as string
              if (!pd || it.payment_received) return null
              const d = Math.ceil((new Date(pd).getTime() - new Date().setHours(0,0,0,0)) / 86400000)
              if (d < 0) return <span className="text-xs text-red-400 font-bold animate-pulse">{-d}日超過!</span>
              if (d <= 5) return <span className="text-xs text-orange-400 font-bold">残{d}日</span>
              return null
            })()}
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-500 w-28">エビデンスURL:</span>
            <input type="url" defaultValue={(it.dashboard_todos?.['payment_evidence_url'] as string) || ''}
              placeholder="https://"
              onBlur={(e) => saveTodoKey(it.id, it.dashboard_todos, 'payment_evidence_url', e.target.value)}
              className="flex-1 px-2 py-0.5 text-xs bg-slate-900 border border-slate-600 rounded text-slate-200 placeholder-slate-600" />
            {(it.dashboard_todos?.['payment_evidence_url'] as string) && (
              <a href={it.dashboard_todos!['payment_evidence_url'] as string} target="_blank" rel="noreferrer" className="text-xs text-blue-400 hover:underline flex-shrink-0">開く</a>
            )}
          </div>
          <div className="flex items-start gap-2">
            <span className="text-xs text-slate-500 w-28 pt-0.5">入金メモ:</span>
            <textarea defaultValue={(it.dashboard_todos?.['payment_memo'] as string) || ''}
              placeholder="入金遅延理由・分割払い・小言など"
              onBlur={(e) => saveTodoKey(it.id, it.dashboard_todos, 'payment_memo', e.target.value)}
              className="flex-1 px-2 py-1 text-xs bg-slate-800 border border-slate-600 rounded text-slate-200 placeholder-slate-600 resize-y"
              rows={2} />
          </div>
        </div>
      )}
    </div>
  )
}

type UrlSectionProps = { it: DeliveryItem; patch: (id: string, u: Record<string, unknown>) => void; saveTodoKey: (id: string, todos: Record<string, unknown> | null | undefined, key: string, val: string) => void }
function UrlSection({ it, patch, saveTodoKey }: UrlSectionProps) {
  const [editing, setEditing] = useState(false)
  const fields: { key: keyof DeliveryItem; label: string; color: string; alertable?: boolean }[] = [
    { key: 'slack_url',         label: 'Slack',      color: 'text-blue-400',    alertable: true },
    { key: 'hubspot_url',       label: 'HubSpot',    color: 'text-orange-400' },
    { key: 'process_sheet_url', label: '工程表',     color: 'text-green-400',   alertable: true },
    { key: 'hearing_sheet_url', label: 'ヒアリング', color: 'text-purple-400',  alertable: true },
  ]
  const hasAny = fields.some(f => !!it[f.key])
  return (
    <div className="border-t border-slate-700/50 pt-3 space-y-2">
      <div className="flex items-center gap-2">
        <p className="text-slate-400 font-bold text-sm">リンク</p>
        <button onClick={() => setEditing(v => !v)}
          className="text-xs px-2 py-0.5 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded">
          {editing ? '閉じる' : 'URL編集'}
        </button>
      </div>
      {!editing && hasAny && (
        <div className="flex flex-wrap gap-3 text-sm">
          {fields.map(f => {
            const v = it[f.key] as string | null | undefined
            return v ? <a key={f.key} href={v} target="_blank" rel="noreferrer" className={`hover:underline ${f.color}`}>{f.label}</a> : null
          })}
        </div>
      )}
      {!editing && !hasAny && <p className="text-xs text-slate-600">リンクなし（URL編集から追加）</p>}
      {editing && (
        <div className="space-y-2">
          {fields.map(f => {
            const v = (it[f.key] as string | null | undefined) || ''
            return (
              <div key={f.key} className="flex items-center gap-2">
                <span className={`text-xs font-medium w-24 flex-shrink-0 ${f.color}`}>{f.label}</span>
                <input type="url" defaultValue={v} placeholder="https://"
                  onBlur={(e) => { if (e.target.value !== v) patch(it.id, { [f.key]: e.target.value || null }) }}
                  className="flex-1 px-2 py-0.5 text-xs bg-slate-900 border border-slate-600 rounded text-slate-200 placeholder-slate-600"
                />
                {v && <a href={v} target="_blank" rel="noreferrer" className={`text-xs hover:underline flex-shrink-0 ${f.color}`}>開く</a>}
                {f.alertable && !v && (
                  <button
                    onClick={() => {
                      const skipKey = `${f.key}_skip`
                      const cur = it.dashboard_todos?.[skipKey]
                      saveTodoKey(it.id, it.dashboard_todos, skipKey, cur ? '' : '1')
                    }}
                    className={`text-xs px-2 py-0.5 rounded font-medium transition-colors flex-shrink-0 ${
                      it.dashboard_todos?.[`${f.key}_skip`] ? 'bg-slate-600 text-slate-300' : 'bg-transparent border border-slate-600 text-slate-500 hover:text-slate-300'
                    }`}
                  >
                    {it.dashboard_todos?.[`${f.key}_skip`] ? '✓ 不要' : '不要'}
                  </button>
                )}
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default function DeliveryPage() {
  const [items, setItems] = useState<DeliveryItem[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'alert' | 'all' | 'done'>('alert')
  const [assigneeFilter, setAssigneeFilter] = useState<string>('米山')
  const [allAssignees, setAllAssignees] = useState<string[]>([])
  const [updating, setUpdating] = useState<string | null>(null)
  const [importing, setImporting] = useState(false)
  const [importResult, setImportResult] = useState<string | null>(null)
  const [csvQueue, setCsvQueue] = useState<File[]>([])
  const [stats, setStats] = useState<{ total: number; lastImport: string | null } | null>(null)
  const [searchQuery, setSearchQuery] = useState<string>('')

  const load = async () => {
    setLoading(true)
    const mode = filter === 'alert' ? '?mode=alert' : ''
    const res = await fetch(`/api/delivery/items${mode}`)
    const d = await res.json()
    let data: DeliveryItem[] = d.items || []
    if (filter === 'done') data = data.filter(i => i.status === 'done')
    if (assigneeFilter !== 'all') data = data.filter(i => i.assignee === assigneeFilter)
    setItems(data.sort((a, b) => a.delivery_due_date.localeCompare(b.delivery_due_date)))
    setLoading(false)
  }

  const loadStats = async () => {
    const res = await fetch('/api/delivery/items')
    const d = await res.json()
    const all: DeliveryItem[] = d.items || []
    const names = Array.from(new Set(all.map((i: DeliveryItem) => i.assignee).filter(Boolean))).sort() as string[]
    setAllAssignees(names)
    const lastImport = all.length > 0 ? all.reduce((a, b) => a.created_at > b.created_at ? a : b).created_at : null
    setStats({ total: all.length, lastImport })
  }

  const patch = async (id: string, updates: Record<string, unknown>) => {
    setUpdating(id)
    setItems(prev => prev.map(it => it.id === id ? { ...it, ...updates } : it))
    await fetch('/api/delivery/items', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, ...updates })
    })
    setUpdating(null)
  }

  const saveTodoKey = async (id: string, currentTodos: Record<string, unknown> | null | undefined, key: string, val: string) => {
    const todos = { ...(currentTodos || {}), [key]: val || null }
    await fetch('/api/delivery/items', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, dashboard_todos: todos })
    })
    setItems(prev => prev.map(it => it.id === id ? { ...it, dashboard_todos: todos } : it))
  }

  const saveMemo = async (id: string, memo: string) => {
    await fetch('/api/delivery/items', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, dashboard_memo: memo })
    })
  }

  const markDone = (id: string) => patch(id, { status: 'done', acknowledged_at: new Date().toISOString() })

  useEffect(() => { load() }, [filter, assigneeFilter])
  useEffect(() => { loadStats() }, [])

  const q = searchQuery.trim().toLowerCase()
  const displayItems = q
    ? items.filter(i =>
        (i.client_name || '').toLowerCase().includes(q) ||
        (i.install_address || '').toLowerCase().includes(q) ||
        (i.product_name || '').toLowerCase().includes(q) ||
        (i.assignee || '').toLowerCase().includes(q) ||
        (i.assignee_name || '').toLowerCase().includes(q) ||
        (i.p400_mtid || '').toLowerCase().includes(q) ||
        (i.p400_tid || '').toLowerCase().includes(q)
      )
    : items

  const overdue  = displayItems.filter(i => getAlertLevel(i.delivery_due_date) === 'overdue')
  const critical = displayItems.filter(i => getAlertLevel(i.delivery_due_date) === 'critical')
  const urgent   = displayItems.filter(i => getAlertLevel(i.delivery_due_date) === 'urgent')

  return (
    <div>
      <div className="mb-6">
        <div className="flex items-center gap-3 flex-wrap">
          <h1 className="text-2xl font-bold text-white">IoT製品 納品予定アラート</h1>
          <a href="https://dms.and-iot.jp/admin/support/login/" target="_blank" rel="noreferrer"
            className="px-3 py-1 text-sm font-medium bg-sky-700 hover:bg-sky-600 text-white rounded-lg transition-colors">
            🔗 DMSログイン
          </a>
          <a href="https://docs.google.com/spreadsheets/d/1FxK4x534LV2sGY54KKtbow1W6iLT0Z_YTzg_R8ba8Go/edit?gid=1821350545#gid=1821350545" target="_blank" rel="noreferrer"
            className="px-3 py-1 text-sm font-medium bg-emerald-700 hover:bg-emerald-600 text-white rounded-lg transition-colors">
            📊 IoTスプレッドシート
          </a>
        </div>
        <p className="text-slate-400 text-base mt-1">納品予定日が近いものから自動で上位表示。CSVを取り込んで最新化してください。</p>
      </div>

      <div className="flex flex-wrap gap-3 mb-4 text-sm">
        <div className="flex items-center gap-2 px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg">
          <span className="text-slate-400">登録件数</span>
          <span className="font-bold text-white">{stats ? `${stats.total}件` : '...'}</span>
        </div>
        {(() => {
          const hoursAgo = stats?.lastImport ? (Date.now() - new Date(stats.lastImport).getTime()) / 3600000 : null
          const isAlert = hoursAgo !== null && hoursAgo >= 24
          return (
            <div className={`flex items-center gap-2 px-3 py-2 rounded-lg border ${isAlert ? 'bg-red-950/80 border-red-400 animate-pulse' : 'bg-slate-800 border-slate-700'}`}>
              {isAlert && <span className="text-lg">⚠️</span>}
              <span className={isAlert ? 'text-red-300' : 'text-slate-400'}>最終取込</span>
              <span className={`font-bold ${isAlert ? 'text-red-200' : 'text-white'}`}>
                {stats?.lastImport ? new Date(stats.lastImport).toLocaleString('ja-JP', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }) : '...'}
              </span>
              {isAlert && <span className="text-red-300 text-xs font-medium">{Math.floor(hoursAgo)}時間未取込</span>}
            </div>
          )
        })()}
      </div>

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
              <p className="font-bold text-red-200 text-lg">緊急！{critical.length}件が3日以内に納品予定</p>
            </div>
          )}
          {urgent.length > 0 && (
            <div className="flex items-center gap-3 px-5 py-4 bg-orange-900/60 border border-orange-500 rounded-xl">
              <span className="text-2xl">⚠️</span>
              <p className="font-bold text-orange-200">{urgent.length}件が1週間以内に納品予定</p>
            </div>
          )}
        </div>
      )}

      <div className="mb-4">
        <input
          type="text"
          value={searchQuery}
          onChange={e => setSearchQuery(e.target.value)}
          placeholder="🔍 会社名・住所・製品名・担当者・MTID/TIDで検索..."
          className="w-full px-4 py-2 rounded-lg bg-slate-700 text-white border border-slate-600 placeholder-slate-400 focus:outline-none focus:border-blue-500 text-sm"
        />
        {searchQuery && (
          <div className="flex items-center gap-2 mt-1.5">
            <span className="text-xs text-slate-400">{displayItems.length}件ヒット</span>
            <button onClick={() => setSearchQuery('')} className="text-xs text-slate-400 hover:text-white underline">クリア</button>
          </div>
        )}
      </div>

      <div className="flex gap-3 mb-5 flex-wrap">
        <button onClick={() => setFilter('alert')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'alert' ? 'bg-red-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>未納品のみ</button>
        <button onClick={() => setFilter('all')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'all' ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>全件表示</button>
        <button onClick={() => setFilter('done')} className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'done' ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>納品完了分</button>
        <select value={assigneeFilter} onChange={e => setAssigneeFilter(e.target.value)} className="px-3 py-2 rounded-lg text-sm bg-slate-700 text-white border border-slate-600">
          <option value="all">全担当者</option>
          {allAssignees.map(a => <option key={a} value={a}>{a}</option>)}
        </select>
        <div className="ml-auto flex items-center gap-2 flex-wrap justify-end">
          {/* キューに溜まったファイル表示 */}
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
          {/* ファイル追加ボタン */}
          <label className="px-3 py-2 rounded-lg text-sm font-medium transition-colors cursor-pointer bg-slate-700 hover:bg-slate-600 text-white">
            ＋CSV追加
            <input type="file" accept=".csv" multiple className="hidden"
              onChange={(e) => {
                const files = Array.from(e.target.files || [])
                if (files.length) setCsvQueue(q => [...q, ...files])
                e.target.value = ''
              }}
            />
          </label>
          {/* 取込実行ボタン */}
          <button
            disabled={importing || csvQueue.length === 0}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${importing || csvQueue.length === 0 ? 'bg-slate-600 text-slate-400 cursor-not-allowed' : 'bg-purple-700 hover:bg-purple-600 text-white'}`}
            onClick={async () => {
              if (!csvQueue.length) return
              setImporting(true); setImportResult(null)
              const texts = await Promise.all(csvQueue.map(f => f.text()))
              const merged = texts.map((t, i) => {
                const lines = t.replace(/\r\n/g, '\n').replace(/\r/g, '\n').split('\n')
                return i === 0 ? lines.join('\n') : lines.slice(1).join('\n')
              }).join('\n')
              const blob = new Blob([merged], { type: 'text/csv' })
              const fd = new FormData(); fd.append('file', blob, 'merged.csv')
              const res = await fetch('/api/delivery/import-csv', { method: 'POST', body: fd })
              const d = await res.json()
              if (d.ok) { setImportResult(`取込完了：${d.imported}件（${csvQueue.length}ファイル結合）`); setCsvQueue([]); loadStats(); load() }
              else { setImportResult(`エラー：${d.error}`) }
              setImporting(false)
            }}
          >
            {importing ? '取込中...' : `取込実行${csvQueue.length > 0 ? `（${csvQueue.length}件）` : ''}`}
          </button>
        </div>
      </div>

      {importResult && (
        <div className={`mb-3 px-4 py-3 rounded-lg text-sm font-medium ${importResult.startsWith('取込') ? 'bg-green-900/60 border border-green-600 text-green-200' : 'bg-red-900/60 border border-red-600 text-red-200'}`}>
          {importResult}
        </div>
      )}

      {loading ? (
        <div className="text-slate-400 text-center py-12">読み込み中...</div>
      ) : displayItems.length === 0 ? (
        <div className="text-slate-400 text-center py-12">
          <p className="text-4xl mb-3">✅</p>
          <p>対象の案件はありません</p>
        </div>
      ) : (
        <div className="space-y-4">
          {displayItems.map(it => {
            const level = getAlertLevel(it.delivery_due_date)
            const s = levelStyle[level]
            const days = daysLeft(it.delivery_due_date)
            const equipItems = it.equipment || []
            const knownNames = ['P400', 'PayCube', 'PayPay']
            const knownEquip = knownNames.map(name => ({ name, eq: equipItems.find(e => e.name === name) })).filter(x => x.eq)
            const otherEquip = equipItems.filter(e => !knownNames.includes(e.name || ''))
            const jitDays = jitLeadDays(it.install_address || '')
            const todoItems = buildTodoItems(it.equipment, it.worker_needed, it.delivery_due_date, jitDays, it.work_date, it.payment_received)
            const getStatus = (name: string) => name === 'P400' ? it.p400_status : name === 'PayCube' ? it.paycube_status : null
            const getField  = (name: string) => name === 'P400' ? 'p400_status' : name === 'PayCube' ? 'paycube_status' : null

            // リードタイム警告（機材リードタイム + JIT）
            const ltWarnings: string[] = []
            if (it.status !== 'done') {
              if (!it.slack_url && !it.dashboard_todos?.['slack_url_skip']) ltWarnings.push('SlackリンクがURLセクションに未登録')
              if (!it.process_sheet_url && !it.dashboard_todos?.['process_sheet_url_skip']) ltWarnings.push('工程表リンクが未登録')
              if (!it.hearing_sheet_url && !it.dashboard_todos?.['hearing_sheet_url_skip']) ltWarnings.push('ヒアリングシートリンクが未登録')
              knownEquip.forEach(({ name }) => {
                const lt = LEAD_TIME[name]; if (!lt) return
                if (days < 0) ltWarnings.push(`${name}：期限超過（リードタイム${lt}日）`)
                else if (days < lt) ltWarnings.push(`${name}：残${days}日 — リードタイム${lt}日、今すぐ発注を`)
              })
              if (it.jitbox_ordered === null || it.jitbox_ordered === undefined) {
                // 未発注のみアラート（発注済み・不要はスキップ）
                if (days < 0) ltWarnings.push(`JITボックス：期限超過（リードタイム${jitDays}日）`)
                else if (days < jitDays) ltWarnings.push(`JITボックス：残${days}日 — 西羵輸送${jitDays}日、今すぐ発注を`)
              }
            }
            const isLocked = !!it.locked

            return (
              <div key={it.id} className={`${s.bg} border ${s.border} rounded-xl p-4 space-y-3 ${isLocked ? 'opacity-60' : ''}`}>

                <div className="flex items-center gap-2 flex-wrap">
                  <span className="text-lg">{s.icon}</span>
                  <span className="font-bold text-white text-base">{it.client_name}</span>
                  {it.status !== 'done'
                    ? <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${s.badge}`}>{s.label}</span>
                    : <span className="text-xs px-2 py-0.5 rounded-full bg-green-700 text-white font-medium">納品完了</span>
                  }
                  {it.progress && <span className="text-xs px-2 py-0.5 rounded-full bg-slate-600 text-slate-200">{it.progress}</span>}
                  {it.missing_in_last_import && <span className="text-xs px-2 py-0.5 rounded-full bg-yellow-800 text-yellow-200">前回取込なし</span>}
                  <button onClick={() => patch(it.id, { locked: !isLocked })}
                    className={`ml-auto px-2 py-0.5 text-xs rounded-lg font-medium transition-colors ${isLocked ? 'bg-red-800 text-red-200 hover:bg-red-700' : 'bg-slate-700 text-slate-400 hover:bg-slate-600'}`}>
                    {isLocked ? '🔒 ロック中' : '🔓 ロック'}
                  </button>
                </div>

                {ltWarnings.length > 0 && (
                  <div className="bg-red-950/80 border border-red-500 rounded-lg px-3 py-2 space-y-1">
                    {ltWarnings.map((w, i) => <p key={i} className="text-red-300 text-sm font-bold animate-pulse">🚨 {w}</p>)}
                  </div>
                )}

                <div className="text-base text-slate-300 space-y-1">
                  <p>納品予定日:{' '}
                    <span className={`font-bold ${level === 'overdue' || level === 'critical' ? 'text-red-300' : level === 'urgent' ? 'text-orange-300' : level === 'warning' ? 'text-yellow-300' : 'text-white'}`}>
                      {it.delivery_due_date}
                    </span>
                    {it.status !== 'done' && <span className="text-slate-400"> （{days < 0 ? `${-days}日超過` : `残 ${days}日`}）</span>}
                  </p>
                  {it.product_name && <p>製品: {it.product_name}{it.quantity ? ` x ${it.quantity}` : ''}</p>}
                  {it.install_address && <p className="text-slate-400 text-sm">設置先: {it.install_address}</p>}
                  {it.assignee && <p>担当: {it.assignee}</p>}
                  {(it.contact_name || it.contact_tel1) && <p>連絡先: {it.contact_name} {it.contact_tel1}</p>}
                  {it.contact_tel2 && <p className="text-slate-400 text-sm">{it.contact_tel2}</p>}
                  {it.notes && <p className="text-slate-400 text-sm">備考: {it.notes}</p>}
                  {(it.p400_mtid || it.p400_tid) && (
                    <p className="text-sm text-slate-300">
                      P400:
                      {it.p400_mtid && <span className="ml-2">MTID <span className="text-white font-mono font-bold">{it.p400_mtid}</span></span>}
                      {it.p400_tid  && <span className="ml-2">TID <span className="text-white font-mono font-bold">{it.p400_tid}</span></span>}
                    </p>
                  )}
                </div>

                {/* 機材ステータス + 日程管理 */}
                {(knownEquip.length > 0 || otherEquip.length > 0) && (
                  <div className="border-t border-slate-700/50 pt-3 space-y-4">
                    <p className="text-slate-400 font-bold text-sm">機材ステータス / 日程管理</p>
                    {knownEquip.map(({ name, eq }) => {
                      const current = getStatus(name); const field = getField(name)
                      return (
                        <div key={name} className="space-y-1">
                          <div className="flex items-center gap-2 flex-wrap">
                            <span className="text-sm font-bold text-slate-200">{name}</span>
                            {eq?.value && <span className="text-slate-400 text-sm">x {eq.value}</span>}
                            {current
                              ? <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${current.includes('完了') || current.includes('済み') ? 'bg-green-800 text-green-200' : 'bg-orange-800 text-orange-200'}`}>{current}</span>
                              : <span className="text-xs px-2 py-0.5 rounded-full bg-slate-700 text-slate-400">未発注</span>
                            }
                          </div>
                          {field && it.status !== 'done' && (
                            <div className="flex flex-wrap gap-1">
                              {EQUIP_STATUSES.map(st => (
                                <button key={st} disabled={updating === it.id}
                                  onClick={() => patch(it.id, { [field]: current === st ? null : st })}
                                  className={`px-3 py-1 text-xs rounded-lg font-medium transition-colors ${current === st ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-500'}`}>
                                  {st}
                                </button>
                              ))}
                            </div>
                          )}
                          {/* 発注日・到着予定日・実到着日 */}
                          <EquipDates
                            name={name}
                            todos={it.dashboard_todos}
                            dueDate={it.delivery_due_date}
                            onSave={(key, val) => saveTodoKey(it.id, it.dashboard_todos, key, val)}
                          />
                        </div>
                      )
                    })}
                    {otherEquip.map((eq, ei) => (
                      <p key={ei} className="text-sm text-slate-300"><span className="text-slate-400">{eq.name}:</span> {eq.value}</p>
                    ))}
                  </div>
                )}

                {/* JITボックス / 作業員 */}
                <div className="border-t border-slate-700/50 pt-3 space-y-3">
                  {/* JIT */}
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-sm text-slate-400">JITボックス:</span>
                    {([
                      { val: null,  label: '未発注', cls: 'bg-slate-700 text-slate-300 hover:bg-slate-600' },
                      { val: true,  label: '発注済み', cls: 'bg-blue-700 text-blue-100 hover:bg-blue-600' },
                      { val: false, label: '不要',   cls: 'bg-slate-600 text-slate-400 hover:bg-slate-500' },
                    ] as { val: boolean | null; label: string; cls: string }[]).map(({ val, label, cls }) => {
                      const active = it.jitbox_ordered === val
                      return (
                        <button key={label} onClick={() => patch(it.id, { jitbox_ordered: val })}
                          className={`px-3 py-1 text-xs rounded-lg font-medium transition-colors border ${active ? `${cls} border-current` : 'bg-transparent border-slate-700 text-slate-500 hover:border-slate-500 hover:text-slate-300'}`}>
                          {label}
                        </button>
                      )
                    })}
                    <span className="text-xs text-slate-600">西羵{jitDays}日</span>
                  </div>

                  {/* 作業員手配 */}
                  <div className="space-y-2">
                    <div className="flex items-center gap-2">
                      <span className="text-sm text-slate-400">作業員手配:</span>
                      <button onClick={() => patch(it.id, { worker_needed: !it.worker_needed })}
                        className={`px-3 py-1 text-xs rounded-lg font-medium transition-colors ${it.worker_needed ? 'bg-orange-700 text-orange-100' : 'bg-slate-700 text-slate-400 hover:bg-slate-600'}`}>
                        {it.worker_needed ? '⚠️ 手配必要' : '不要'}
                      </button>
                    </div>

                    {it.worker_needed && (
                      <div className="bg-slate-900/50 border border-slate-700 rounded-lg p-3 space-y-2">

                        {/* 作業日 */}
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-slate-500 w-24">作業日:</span>
                          <input type="date" defaultValue={it.work_date || ''}
                            onBlur={(e) => { if (e.target.value !== (it.work_date || '')) patch(it.id, { work_date: e.target.value || null }) }}
                            className="px-2 py-0.5 text-xs bg-slate-800 border border-slate-600 rounded text-white"
                          />
                        </div>

                        {/* 作業開始時間 */}
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-slate-500 w-24">作業開始:</span>
                          <input type="time" defaultValue={(it as any).work_start_time || ''}
                            onBlur={(e) => { if (e.target.value !== ((it as any).work_start_time || '')) patch(it.id, { work_start_time: e.target.value || null }) }}
                            className="px-2 py-0.5 text-xs bg-slate-800 border border-slate-600 rounded text-white"
                          />
                        </div>

                        {/* 見積もりステータス */}
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="text-xs text-slate-500 w-24">見積もり:</span>
                          {['見積待ち', '見積 OK', '発注済み', '作業完了'].map(st => {
                            const cur = (it.dashboard_todos?.['worker_estimate_status'] as string) || ''
                            return (
                              <button key={st}
                                onClick={() => saveTodoKey(it.id, it.dashboard_todos, 'worker_estimate_status', cur === st ? '' : st)}
                                className={`px-2 py-0.5 text-xs rounded font-medium transition-colors ${
                                  cur === st ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-500'
                                }`}>{st}</button>
                            )
                          })}
                        </div>

                        {/* 担当作業員名 */}
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-slate-500 w-24">担当者名:</span>
                          <input type="text"
                            defaultValue={(it.dashboard_todos?.['worker_name'] as string) || ''}
                            placeholder="作業員名・会社名"
                            onBlur={(e) => saveTodoKey(it.id, it.dashboard_todos, 'worker_name', e.target.value)}
                            className="flex-1 px-2 py-0.5 text-xs bg-slate-800 border border-slate-600 rounded text-slate-200 placeholder-slate-600"
                          />
                        </div>

                        {/* 連絡先 */}
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-slate-500 w-24">連絡先:</span>
                          <input type="text"
                            defaultValue={(it.dashboard_todos?.['worker_contact'] as string) || ''}
                            placeholder="電話・メール・連絡方法"
                            onBlur={(e) => saveTodoKey(it.id, it.dashboard_todos, 'worker_contact', e.target.value)}
                            className="flex-1 px-2 py-0.5 text-xs bg-slate-800 border border-slate-600 rounded text-slate-200 placeholder-slate-600"
                          />
                        </div>

                        {/* 見積金額 */}
                        <div className="flex items-center gap-2">
                          <span className="text-xs text-slate-500 w-24">見積金額:</span>
                          <input type="text"
                            defaultValue={(it.dashboard_todos?.['worker_estimate_amount'] as string) || ''}
                            placeholder="例: 35,000円"
                            onBlur={(e) => saveTodoKey(it.id, it.dashboard_todos, 'worker_estimate_amount', e.target.value)}
                            className="w-40 px-2 py-0.5 text-xs bg-slate-800 border border-slate-600 rounded text-slate-200 placeholder-slate-600"
                          />
                        </div>

                        {/* メモ */}
                        <div className="flex items-start gap-2">
                          <span className="text-xs text-slate-500 w-24 pt-0.5">メモ:</span>
                          <textarea
                            defaultValue={(it.dashboard_todos?.['worker_memo'] as string) || ''}
                            placeholder="見積待ち理由・小言・特記事項など"
                            onBlur={(e) => saveTodoKey(it.id, it.dashboard_todos, 'worker_memo', e.target.value)}
                            className="flex-1 px-2 py-1 text-xs bg-slate-800 border border-slate-600 rounded text-slate-200 placeholder-slate-600 resize-y"
                            rows={2}
                          />
                        </div>

                        {/* DBに保存済みの連絡先情報（CSV由来） */}
                        {it.worker_contacts && it.worker_contacts.filter(c => c.name || c.tel || c.email).length > 0 && (
                          <div className="border-t border-slate-700/50 pt-2">
                            <p className="text-xs text-slate-500 mb-1">登録済み作業員情報 (CSV):</p>
                            {it.worker_contacts.filter(c => c.name || c.tel || c.email).map((c, ci) => (
                              <p key={ci} className="text-slate-300 text-xs ml-1">{[c.name, c.tel, c.email].filter(Boolean).join(' / ')}</p>
                            ))}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>

                {/* 入金管理 折りたたみ */}
                <PaymentSection it={it} patch={patch} saveTodoKey={saveTodoKey} />


                <UrlSection it={it} patch={patch} saveTodoKey={saveTodoKey} />

                <div className="flex items-center gap-2 border-t border-slate-700/50 pt-2">
                  <span className="text-sm text-slate-400">納品予定日変更:</span>
                  <input type="date" defaultValue={it.delivery_due_date}
                    onBlur={(e) => { if (e.target.value && e.target.value !== it.delivery_due_date) patch(it.id, { delivery_due_date: e.target.value }) }}
                    className="px-2 py-1 text-sm bg-slate-800 border border-slate-600 rounded text-white"
                  />
                </div>

                <div className="border-t border-slate-700/50 pt-2 space-y-2">
                  <p className="text-slate-400 font-bold text-sm">次にすべきこと</p>
                  <div className="space-y-1.5">
                    {todoItems.map(({ label, deadlineDate, urgent }) => {
                      const isJit = label.startsWith('JITボックス')
                      const jitDone = isJit && it.jitbox_ordered !== null && it.jitbox_ordered !== undefined
                      const isWorker = label === '作業員 手配'
                      const workerDone = isWorker && (it.dashboard_todos?.['worker_estimate_status'] as string) === '作業完了'
                      const checked = jitDone || workerDone || !!(it.dashboard_todos?.[label] as boolean)
                      const today2 = new Date(); today2.setHours(0,0,0,0)
                      const dLeft = deadlineDate ? Math.ceil((new Date(deadlineDate).getTime() - today2.getTime()) / 86400000) : null
                      return (
                        <label key={label} className="flex items-center gap-2 cursor-pointer text-sm hover:text-white">
                          <input type="checkbox" checked={checked}
                            onChange={() => { if (!jitDone && !workerDone) saveTodoKey(it.id, it.dashboard_todos, label, checked ? '' : '1') }}
                            disabled={jitDone || workerDone}
                            className="w-4 h-4 accent-blue-500 flex-shrink-0 disabled:opacity-50"
                          />
                          <span className={checked ? 'line-through text-slate-500' : 'text-slate-300'}>{label}</span>
                          {deadlineDate && !checked && (
                            <span className={`text-xs ml-1 font-medium ${
                              dLeft !== null && dLeft < 0 ? 'text-red-400 animate-pulse' :
                              urgent ? 'text-orange-400 font-bold' : 'text-slate-500'
                            }`}>
                              {dLeft !== null && dLeft < 0 ? `期限${-dLeft}日超過` :
                               dLeft === 0 ? '今日まで' :
                               `${deadlineDate}まで（残${dLeft}日）`}
                            </span>
                          )}
                        </label>
                      )
                    })}
                  </div>
                </div>

                <div className="flex gap-3 items-end border-t border-slate-700/50 pt-2">
                  <textarea key={`memo-${it.id}`} defaultValue={it.dashboard_memo || ''}
                    placeholder="メモ・状況・連絡事項など"
                    onBlur={(e) => saveMemo(it.id, e.target.value)}
                    className="flex-1 px-3 py-2 text-sm bg-slate-900/60 border border-slate-700 rounded-lg text-slate-200 placeholder-slate-500 resize-y"
                    rows={3}
                  />
                  {it.status !== 'done' && (
                    <button disabled={updating === it.id} onClick={() => markDone(it.id)}
                      className="px-4 py-2 bg-green-700 hover:bg-green-600 disabled:opacity-50 text-white text-sm rounded-lg font-medium transition-colors whitespace-nowrap">
                      納品完了にする
                    </button>
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
