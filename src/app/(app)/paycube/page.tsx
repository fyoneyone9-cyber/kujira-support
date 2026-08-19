'use client'

import { useEffect, useState } from 'react'

type Contract = {
  id: string
  client_name: string
  management_no: string
  plan_name: string
  plan_type: string
  start_date: string
  end_date: string
  status: string
  contacted_at: string | null
  renewed_at: string | null
  notes: string
  created_at: string
}

type AlertLevel = 'critical' | 'urgent' | 'warning' | 'ok'

function getAlertLevel(endDate: string): AlertLevel {
  const today = new Date()
  const end = new Date(endDate)
  const diffDays = Math.ceil((end.getTime() - today.getTime()) / 86400000)
  if (diffDays <= 14) return 'critical'
  if (diffDays <= 30) return 'urgent'
  if (diffDays <= 60) return 'warning'
  return 'ok'
}

function daysLeft(endDate: string): number {
  const today = new Date()
  const end = new Date(endDate)
  return Math.ceil((end.getTime() - today.getTime()) / 86400000)
}

const levelStyle: Record<AlertLevel, { bg: string; border: string; badge: string; label: string; icon: string }> = {
  critical: { bg: 'bg-red-950/60', border: 'border-red-500', badge: 'bg-red-600 text-white', label: '🔴 緊急', icon: '🚨' },
  urgent:   { bg: 'bg-orange-950/60', border: 'border-orange-500', badge: 'bg-orange-500 text-white', label: '🟠 要対忁E, icon: '⚠�E�E },
  warning:  { bg: 'bg-yellow-950/60', border: 'border-yellow-500', badge: 'bg-yellow-600 text-white', label: '🟡 注愁E, icon: '📋' },
  ok:       { bg: 'bg-slate-800', border: 'border-slate-700', badge: 'bg-slate-600 text-slate-200', label: '✁E余裕あめE, icon: '✁E },
}

const statusLabel: Record<string, string> = {
  active: '未対忁E,
  alerted: '⚠�E�Eアラート渁E,
  contacted: '📞 連絡渁E,
  renewed: '✁E更新完亁E,
  expired: '❁E期限刁E��',
  needs_review: '🔍 要確誁E,
}

function exportCSV(contracts: Contract[], filter: string) {
  const headers = ['設置先名', '管琁E��号', '保守�E容', '保守種別', '開始日', '終亁E��', '残日数', 'スチE�Eタス', '連絡済日', '更新完亁E��', '備老E]
  const statusLabel: Record<string, string> = {
    active: '未対忁E, alerted: 'アラート渁E, contacted: '連絡渁E,
    renewed: '更新完亁E, expired: '期限刁E��', needs_review: '要確誁E,
  }
  const rows = contracts.map(c => {
    const days = Math.ceil((new Date(c.end_date).getTime() - new Date().getTime()) / 86400000)
    return [
      c.client_name,
      c.management_no,
      c.plan_name,
      c.plan_type === 'free' ? '無償保宁E : '有償保宁E,
      c.start_date,
      c.end_date,
      String(days),
      statusLabel[c.status] || c.status,
      c.contacted_at ? new Date(c.contacted_at).toLocaleDateString('ja-JP') : '',
      c.renewed_at ? new Date(c.renewed_at).toLocaleDateString('ja-JP') : '',
      c.notes,
    ].map(v => `"${(v || '').replace(/"/g, '""')}"`)
  })
  const bom = '\uFEFF'
  const csv = bom + [headers.join(','), ...rows.map(r => r.join(','))].join('\n')
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  const label = filter === 'alert' ? 'アラート対象' : filter === 'review' ? '要確認物件' : '全件'
  const date = new Date().toISOString().slice(0, 10).replace(/-/g, '')
  a.href = url
  a.download = `paycube_${label}_${date}.csv`
  a.click()
  URL.revokeObjectURL(url)
}

export default function PayCubePage() {
  const [contracts, setContracts] = useState<Contract[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'alert' | 'review' | 'all'>('alert')
  const [updating, setUpdating] = useState<string | null>(null)
  const [showAdd, setShowAdd] = useState(false)
  const [importing, setImporting] = useState(false)
  const [importResult, setImportResult] = useState<string | null>(null)
  const [stats, setStats] = useState<{ total: number; lastImport: string | null } | null>(null)
  const [form, setForm] = useState({
    client_name: '', management_no: '', plan_name: '', plan_type: 'paid',
    start_date: '', end_date: '', notes: '', product_type: '',
    serial_no_hard: '', serial_no_bill: ''
  })

  const load = async () => {
    setLoading(true)
    const mode = filter === 'alert' ? '?mode=alert' : filter === 'review' ? '?mode=review' : ''
    const res = await fetch(`/api/paycube/contracts${mode}`)
    const d = await res.json()
    setContracts(d.contracts || [])
    setLoading(false)
  }

  const loadStats = async () => {
    const res = await fetch('/api/paycube/contracts')
    const d = await res.json()
    const all: Contract[] = d.contracts || []
    const lastImport = all.length > 0
      ? all.reduce((a, b) => a.created_at > b.created_at ? a : b).created_at
      : null
    setStats({ total: all.length, lastImport })
  }

  useEffect(() => { load() }, [filter])
  useEffect(() => { loadStats() }, [])

  const updateStatus = async (id: string, status: string) => {
    setUpdating(id)
    const extra: Record<string, string> = {}
    if (status === 'contacted') extra.contacted_at = new Date().toISOString()
    if (status === 'renewed') extra.renewed_at = new Date().toISOString()
    await fetch('/api/paycube/contracts', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, status, ...extra })
    })
    setUpdating(null)
    load()
  }

  const addContract = async () => {
    if (!form.client_name || !form.end_date) return alert('設置先名と保守終亁E��は忁E��でぁE)
    await fetch('/api/paycube/contracts', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    })
    setShowAdd(false)
    setForm({ client_name: '', management_no: '', plan_name: '', plan_type: 'paid', start_date: '', end_date: '', notes: '', product_type: '', serial_no_hard: '', serial_no_bill: '' })
    load()
  }

  const critical = contracts.filter(c => getAlertLevel(c.end_date) === 'critical')
  const urgent   = contracts.filter(c => getAlertLevel(c.end_date) === 'urgent')
  const warning  = contracts.filter(c => getAlertLevel(c.end_date) === 'warning')
  const ok       = contracts.filter(c => getAlertLevel(c.end_date) === 'ok')

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">🔔 PayCube保守期限アラーチE/h1>
        <p className="text-slate-400 text-base mt-1">2ヶ月前から自動アラート。期限�Eれ前に顧客連絡・更新手続きを完亁E��てください、E/p>
      </div>

      {/* チE�EタスチE�Eタスバ�E */}
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
        <div className="flex items-center gap-2 px-3 py-2 bg-slate-800 border border-slate-700 rounded-lg">
          <span className="text-slate-400">🔗 チE�Eタソース</span>
          <a
            href="https://docs.google.com/spreadsheets/d/107wEIMY-wiIcPg0K_cDfyVGajKoFmluto8wJdSbqeOg/edit?gid=849544635#gid=849544635"
            target="_blank"
            rel="noopener noreferrer"
            className="text-blue-400 hover:underline font-medium"
          >
            進捗管琁E��ーチEↁE          </a>
          <span className="text-slate-500">�E�手動CSV取込�E�E/span>
        </div>
      </div>

      {/* アラートサマリーバナー */}
      {(critical.length > 0 || urgent.length > 0 || warning.length > 0) && filter === 'alert' && (
        <div className="mb-6 space-y-3">
          {critical.length > 0 && (
            <div className="flex items-center gap-3 px-5 py-4 bg-red-900/80 border border-red-500 rounded-xl animate-pulse">
              <span className="text-2xl">🚨</span>
              <div>
                <p className="font-bold text-red-200 text-lg">緊急�E�{critical.length}件ぁE週間以冁E��期限刁E��</p>
                <p className="text-red-300 text-sm">即座に顧客連絡・保守シスチE��への更新登録が忁E��でぁE/p>
              </div>
            </div>
          )}
          {urgent.length > 0 && (
            <div className="flex items-center gap-3 px-5 py-4 bg-orange-900/60 border border-orange-500 rounded-xl">
              <span className="text-2xl">⚠�E�E/span>
              <div>
                <p className="font-bold text-orange-200">{urgent.length}件ぁEヶ月以冁E��期限刁E��</p>
                <p className="text-orange-300 text-sm">顧客への連絡を開始してください</p>
              </div>
            </div>
          )}
          {warning.length > 0 && (
            <div className="flex items-center gap-3 px-5 py-4 bg-yellow-900/40 border border-yellow-600 rounded-xl">
              <span className="text-2xl">📋</span>
              <div>
                <p className="font-bold text-yellow-200">{warning.length}件ぁEヶ月以冁E��期限刁E��</p>
                <p className="text-yellow-300 text-sm">準備を進めてください�E�無償保守�E場合�E顧客確認が忁E��E��E/p>
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
          🔔 アラート対象のみ ({loading ? '...' : contracts.filter(c => getAlertLevel(c.end_date) !== 'ok').length})
        </button>
        <button
          onClick={() => setFilter('review')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'review' ? 'bg-purple-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}
        >
          🔍 要確認物件 (36)
        </button>
        <button
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'all' ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}
        >
          📋 全件表示
        </button>
        <button
          onClick={() => fetch('/api/paycube/check-alerts').then(() => load())}
          className="px-4 py-2 rounded-lg text-sm font-medium bg-slate-700 text-slate-300 hover:bg-slate-600 transition-colors"
        >
          🔄 手動チェチE��実衁E        </button>
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
              const res = await fetch('/api/paycube/import-csv', { method: 'POST', body: fd })
              const d = await res.json()
              if (d.ok) {
                setImportResult(`✁E取込完亁E��有効${d.imported}件 �E�E要確誁E{d.needs_review}件`)
                loadStats()
                load()
              } else {
                setImportResult(`❁Eエラー�E�E{d.error}`)
              }
              setImporting(false)
              e.target.value = ''
            }}
          />
        </label>
        <button
          onClick={() => exportCSV(contracts, filter)}
          className="px-4 py-2 rounded-lg text-sm font-medium bg-teal-700 text-white hover:bg-teal-600 transition-colors"
        >
          📤 CSVエクスポ�EチE        </button>
        <button
          onClick={() => setShowAdd(!showAdd)}
          className="px-4 py-2 rounded-lg text-sm font-medium bg-green-700 text-white hover:bg-green-600 transition-colors"
        >
          �E�E契紁E��録
        </button>
      </div>

      {/* 取込結果 */}
      {importResult && (
        <div className={`mb-3 px-4 py-3 rounded-lg text-sm font-medium ${importResult.startsWith('✁E) ? 'bg-green-900/60 border border-green-600 text-green-200' : 'bg-red-900/60 border border-red-600 text-red-200'}`}>
          {importResult}
          <span className="ml-2 text-xs text-slate-400">スプレチE��シートをCSVでダウンローチEↁEこ�Eボタンで再取込すれば常に最新状態になりまぁE/span>
        </div>
      )}

      {/* 新規登録フォーム */}
      {showAdd && (
        <div className="mb-6 p-5 bg-slate-800 border border-slate-600 rounded-xl">
          <h2 className="font-bold text-white mb-4">📝 PayCube契紁E��録</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {[
              { key: 'client_name', label: '設置先名 *', type: 'text', required: true },
              { key: 'management_no', label: '管琁E��号(コンラチE��ス)', type: 'text' },
              { key: 'product_type', label: '製品タイチE, type: 'text', placeholder: 'キュービック垁E黁E' },
              { key: 'plan_name', label: '保守サービス冁E��', type: 'text', placeholder: '1年目:コールセンター利用' },
              { key: 'start_date', label: '保守開始日', type: 'date' },
              { key: 'end_date', label: '保守終亁E�� *', type: 'date', required: true },
              { key: 'serial_no_hard', label: '硬質ユニットシリアルNo.', type: 'text' },
              { key: 'serial_no_bill', label: '紙幣ユニットシリアルNo.', type: 'text' },
            ].map(({ key, label, type, required, placeholder }) => (
              <div key={key}>
                <label className="text-xs text-slate-400 mb-1 block">{label}</label>
                <input
                  type={type}
                  value={(form as Record<string, string>)[key]}
                  placeholder={placeholder}
                  onChange={e => setForm(f => ({ ...f, [key]: e.target.value }))}
                  className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:border-blue-500 focus:outline-none"
                />
              </div>
            ))}
            <div>
              <label className="text-xs text-slate-400 mb-1 block">保守種別</label>
              <select
                value={form.plan_type}
                onChange={e => setForm(f => ({ ...f, plan_type: e.target.value }))}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm"
              >
                <option value="paid">有償保宁E/option>
                <option value="free">無償保宁E/option>
              </select>
            </div>
            <div>
              <label className="text-xs text-slate-400 mb-1 block">備老E/label>
              <input
                type="text"
                value={form.notes}
                onChange={e => setForm(f => ({ ...f, notes: e.target.value }))}
                className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm"
              />
            </div>
          </div>
          <div className="flex gap-3 mt-4">
            <button onClick={addContract} className="px-5 py-2 bg-green-600 hover:bg-green-500 text-white rounded-lg text-sm font-medium">登録</button>
            <button onClick={() => setShowAdd(false)} className="px-5 py-2 bg-slate-600 hover:bg-slate-500 text-white rounded-lg text-sm font-medium">キャンセル</button>
          </div>
        </div>
      )}

      {/* 契紁E��覧 */}
      {loading ? (
        <div className="text-slate-400 text-center py-12">読み込み中...</div>
      ) : contracts.length === 0 ? (
        <div className="text-slate-400 text-center py-12">
          <p className="text-4xl mb-3">✁E/p>
          <p>アラート対象の契紁E�Eありません</p>
        </div>
      ) : (
        <div className="space-y-3">
          {contracts.map(c => {
            const level = getAlertLevel(c.end_date)
            const s = levelStyle[level]
            const days = daysLeft(c.end_date)
            return (
              <div key={c.id} className={`${s.bg} border ${s.border} rounded-xl p-4`}>
                <div className="flex items-start justify-between gap-3 flex-wrap">
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap mb-1">
                      <span className="text-lg">{s.icon}</span>
                      <span className="font-bold text-white text-base">{c.client_name}</span>
                      <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${s.badge}`}>{s.label}</span>
                      {c.plan_type === 'free' && (
                        <span className="text-xs px-2 py-0.5 rounded-full bg-purple-700 text-purple-100 font-medium">無償保守⚠要確誁E/span>
                      )}
                      <span className="text-xs px-2 py-0.5 rounded-full bg-slate-600 text-slate-200">{statusLabel[c.status] || c.status}</span>
                    </div>
                    <div className="text-base text-slate-300 space-y-1">
                      <p>📅 保守終亁E��: <span className={`font-bold ${level === 'critical' ? 'text-red-300' : level === 'urgent' ? 'text-orange-300' : level === 'warning' ? 'text-yellow-300' : 'text-white'}`}>{c.end_date}</span> <span className="text-slate-400">(殁E{days}日)</span></p>
                      {c.plan_name && <p>📋 プラン: {c.plan_name}</p>}
                      {c.management_no && <p>🔢 管琁E��号: {c.management_no}</p>}
                      {c.contacted_at && <p>📞 連絡渁E {new Date(c.contacted_at).toLocaleDateString('ja-JP')}</p>}
                      {c.notes && <p className="text-slate-400">📝 {c.notes}</p>}
                    </div>
                  </div>
                  {/* アクションボタン */}
                  <div className="flex flex-col gap-2 min-w-fit">
                    {c.status !== 'contacted' && c.status !== 'renewed' && (
                      <button
                        disabled={updating === c.id}
                        onClick={() => updateStatus(c.id, 'contacted')}
                        className="px-4 py-2 bg-blue-700 hover:bg-blue-600 text-white text-sm rounded-lg font-medium transition-colors whitespace-nowrap"
                      >
                        📞 連絡済みにする
                      </button>
                    )}
                    {c.status !== 'renewed' && (
                      <button
                        disabled={updating === c.id}
                        onClick={() => updateStatus(c.id, 'renewed')}
                        className="px-4 py-2 bg-green-700 hover:bg-green-600 text-white text-sm rounded-lg font-medium transition-colors whitespace-nowrap"
                      >
                        ✁E更新完亁E                      </button>
                    )}
                    <a
                      href="https://dist.paycube-service.com/paycube/customer_detail.php"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-4 py-2 bg-slate-600 hover:bg-slate-500 text-white text-sm rounded-lg font-medium transition-colors text-center whitespace-nowrap"
                    >
                      🔗 保守シスチE��
                    </a>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* 関連リンク */}
      <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-3">
        {[
          { label: 'PayCube保守シスチE���E�ログイン�E�E, url: 'https://dist.paycube-service.com/paycube/customer_detail.php', icon: '🔐', desc: 'ID/PW: devicee' },
          { label: '進捗管琁E��ーチE, url: 'https://docs.google.com/spreadsheets/d/107wEIMY-wiIcPg0K_cDfyVGajKoFmluto8wJdSbqeOg/edit?gid=849544635#gid=849544635', icon: '📊', desc: 'K列まで入劁EↁE野田さんへ連絡' },
          { label: 'PayCube保守�Eニュアル', url: '/manuals', icon: '📋', desc: '操作手頁E�Eエスカレーション基溁E },
          { label: 'MailDealer�E�メール対応！E, url: 'https://mdjack.maildealer.jp/index.php', icon: '📨', desc: '顧客への連絡はこちらかめE },
          { label: 'Zoom Phone�E�架電�E�E, url: 'https://app.zoom.us/wc/phone', icon: '📞', desc: '無償�E有償刁E��の顧客連絡' },
          { label: 'くじらCRM', url: 'https://d1zlma8f7wwwsg.cloudfront.net/login', icon: '🐋', desc: '顧客惁E��の確誁E },
          { label: '工程管琁E��ーチE, url: 'https://docs.google.com/spreadsheets/d/1GiEvK-KLB7rl1lrCn-Llgl9H6W4m2PuZJXby2RqIuMc/edit?gid=602309486#gid=602309486', icon: '📈', desc: '全体進捗�E管琁E },
          { label: 'くじら社冁Eiki', url: 'https://www.notion.so/kujira-device-agency/Wiki-dc27874409f24d549bb439103f852185', icon: '📖', desc: 'Notion Wiki' },
        ].map(link => (
          <a
            key={link.url}
            href={link.url}
            target={link.url.startsWith('http') ? '_blank' : undefined}
            rel={link.url.startsWith('http') ? 'noopener noreferrer' : undefined}
            className="flex items-center gap-3 px-4 py-3 bg-slate-800 hover:bg-slate-700 border border-slate-700 hover:border-slate-500 rounded-xl transition-colors group"
          >
            <span className="text-2xl">{link.icon}</span>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-slate-200 group-hover:text-white transition-colors">{link.label}</p>
              <p className="text-xs text-slate-500">{link.desc}</p>
            </div>
            <span className="text-slate-500 text-xs">ↁE/span>
          </a>
        ))}
      </div>

      {/* ログイン惁E�� */}
      <div className="mt-4 p-5 bg-slate-800 border border-slate-700 rounded-xl">
        <h3 className="font-bold text-white mb-3">🔐 保守シスチE�� ログイン惁E��</h3>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 text-sm">
          <div className="bg-slate-700/50 rounded-lg px-4 py-3">
            <p className="text-slate-400 text-xs mb-1">URL</p>
            <a href="https://dist.paycube-service.com/paycube/index.php" target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline break-all">https://dist.paycube-service.com/paycube/index.php</a>
          </div>
          <div className="bg-slate-700/50 rounded-lg px-4 py-3">
            <p className="text-slate-400 text-xs mb-1">ログインID</p>
            <p className="text-white font-mono font-bold text-lg">devicee</p>
          </div>
          <div className="bg-slate-700/50 rounded-lg px-4 py-3">
            <p className="text-slate-400 text-xs mb-1">パスワーチE/p>
            <p className="text-white font-mono font-bold text-lg">devicee</p>
          </div>
        </div>
      </div>

      {/* 保守更新フロー */}
      <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
        <div className="p-5 bg-slate-800 border border-blue-800 rounded-xl">
          <h3 className="font-bold text-white mb-3">🔄 保守更新フロー</h3>
          <ol className="space-y-2 text-sm text-slate-300">
            {[
              'ログイン後、画面下部「保守期限」セクションを確誁E,
              '「今月」「来月」「�E来月」�E3タブを全部チェチE���E�漏れ防止�E�E,
              '設置先名�E�青斁E��リンク�E�をクリチE��',
              '右側「登録」�EタンをクリチE��',
              '「保守サービス冁E��」�Eルダウンでプランを選抁E,
              '「登録」�Eタンで完亁E,
              '進捗管琁E��ート�EK列まで入劁E,
              '野田さんへ連絡',
            ].map((step, i) => (
              <li key={i} className="flex gap-2">
                <span className="text-blue-400 font-bold min-w-[20px]">{i + 1}.</span>
                <span>{step}</span>
              </li>
            ))}
          </ol>
          <div className="mt-4 space-y-2">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wide">プラン別対忁E/p>
            <div className="flex gap-2 text-xs">
              <span className="px-2 py-1 bg-green-900 text-green-200 rounded">有償保宁E/span>
              <span className="text-slate-400">顧客連絡不要EↁE同�Eランで期間延長</span>
            </div>
            <div className="flex gap-2 text-xs">
              <span className="px-2 py-1 bg-purple-900 text-purple-200 rounded">無償保宁E/span>
              <span className="text-slate-400">顧客連絡忁E��EↁE加入意思�E希望プランを確認してから登録</span>
            </div>
          </div>
        </div>

        <div className="p-5 bg-slate-800 border border-green-800 rounded-xl">
          <h3 className="font-bold text-white mb-3">➁E新規登録フロー</h3>
          <ol className="space-y-2 text-sm text-slate-300">
            {[
              'メニューから「新規登録」を選抁E,
              '不�Eな頁E��は進捗管琁E��ートを参�Eして補宁E,
              '忁E��頁E��を�E力（赤マ�Eク付き�E�E,
              '「保守申請に進む」をクリチE��',
              '無償保守�Eそ�Eまま「申請」�Eタンで完亁E,
              '進捗管琁E��ーチE列まで入劁E,
              '野田さんへ連絡',
            ].map((step, i) => (
              <li key={i} className="flex gap-2">
                <span className="text-green-400 font-bold min-w-[20px]">{i + 1}.</span>
                <span>{step}</span>
              </li>
            ))}
          </ol>
          <div className="mt-4 p-3 bg-yellow-900/40 border border-yellow-700 rounded-lg text-xs text-yellow-200">
            ⚠�E�EシリアルNo.不�Eの場合�E <span className="font-mono font-bold">999999999</span>�E�E桁E��を入劁E          </div>
        </div>
      </div>

      {/* エスカレーション */}
      <div className="mt-4 p-5 bg-slate-800 border border-slate-700 rounded-xl">
        <h3 className="font-bold text-white mb-3">🚨 エスカレーション基溁E/h3>
        <div className="space-y-2 text-sm">
          <div className="flex items-start gap-3 p-3 bg-red-950/50 border border-red-800 rounded-lg">
            <span>🔴</span>
            <div><p className="text-red-300 font-medium">保守期間が刁E��た状態での再加入</p><p className="text-slate-400 text-xs mt-0.5">シスチE��登録不可 ↁE直ちに吉井さんへエスカレーション</p></div>
          </div>
          <div className="flex items-start gap-3 p-3 bg-yellow-950/50 border border-yellow-800 rounded-lg">
            <span>🟡</span>
            <div><p className="text-yellow-300 font-medium">保守�E途中解紁E�E別プランへの刁E��替ぁE/p><p className="text-slate-400 text-xs mt-0.5">自己判断せず ↁE吉井さんへエスカレーション</p></div>
          </div>
          <div className="flex items-start gap-3 p-3 bg-green-950/50 border border-green-800 rounded-lg">
            <span>✁E/span>
            <div><p className="text-green-300 font-medium">通常の更新・新規登録</p><p className="text-slate-400 text-xs mt-0.5">進捗管琁E��ート記�E ↁE野田さんへ連絡</p></div>
          </div>
        </div>
      </div>
      {/* 要確認バナ�E */}
      {filter === 'review' && contracts.length > 0 && (
        <div className="mb-4 p-4 bg-purple-950/60 border border-purple-600 rounded-xl text-sm text-purple-200">
          <p className="font-bold mb-1">🔍 要確認物件とは</p>
          <p className="text-purple-300 text-xs">保守終亁E��チE�Eタなし、また�E保守期限�Eれ�E物件です。保守シスチE��で現状を確認し、対応を判断してください。期限�Eれ後�E再加入は<strong>吉井さんへエスカレーション</strong>が忁E��です、E/p>
        </div>
      )}

      {/* アラート発生時の対応フロー */}
      <div className="mt-4 p-5 bg-slate-800 border border-slate-700 rounded-xl">
        <h3 className="font-bold text-white mb-4">🚨 アラート発生時の対応フロー</h3>

        {/* 現在のプラン刁E��E*/}
        <div className="mb-5">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wide mb-3">STEP 1 ── 現在のプランを確認すめE/p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="p-4 bg-green-950/50 border border-green-700 rounded-xl">
              <p className="font-bold text-green-300 mb-2">✁E有償保守�E場吁E/p>
              <ul className="text-sm text-slate-300 space-y-1">
                <li>ↁE顧客への連絡 <span className="text-green-400 font-medium">不要E/span></li>
                <li>ↁE同�Eランで期間延長して登録するだぁE/li>
                <li className="text-slate-500 text-xs mt-1">※ STEP 3�E�シスチE��登録�E�へ進む</li>
              </ul>
            </div>
            <div className="p-4 bg-purple-950/50 border border-purple-700 rounded-xl">
              <p className="font-bold text-purple-300 mb-2">⚠�E�E無償保守�E場吁E/p>
              <ul className="text-sm text-slate-300 space-y-1">
                <li>ↁE顧客への連絡 <span className="text-red-400 font-medium">忁E��E/span></li>
                <li>ↁE加入意思と希望プランを確認してから登録</li>
                <li className="text-slate-500 text-xs mt-1">※ STEP 2�E�顧客連絡�E�へ進む</li>
              </ul>
            </div>
          </div>
        </div>

        {/* STEP 2 無償保守�Eみ */}
        <div className="mb-5 pl-4 border-l-2 border-purple-700">
          <p className="text-xs font-bold text-purple-400 uppercase tracking-wide mb-3">STEP 2 ── 顧客へ連絡�E�無償保守�Eみ�E�E/p>
          <div className="space-y-2 text-sm text-slate-300">
            <div className="flex gap-3 items-start">
              <span className="text-purple-400 font-bold min-w-[24px]">①</span>
              <div>
                <p>MailDealer or Zoom Phone で顧客へ連絡</p>
                <p className="text-xs text-slate-500 mt-0.5">「無償保証期間が、E��、E��に終亁E��ます。有償保守への移行につぁE��ご案�EぁE��します、E/p>
              </div>
            </div>
            <div className="flex gap-3 items-start">
              <span className="text-purple-400 font-bold min-w-[24px]">②</span>
              <div>
                <p>希望プランの確認（下記料金表を参老E��案�E�E�E/p>
                <p className="text-xs text-slate-500 mt-0.5">コールセンターのみ ¥28,800 / オンサイト込 ¥57,600 / 全部入めE¥81,600</p>
              </div>
            </div>
            <div className="flex gap-3 items-start">
              <span className="text-purple-400 font-bold min-w-[24px]">③</span>
              <div>
                <p>見積書PDFを添付してメール送仁E/p>
                <p className="text-xs text-slate-500 mt-0.5">ↁE下�EメールチE��プレートを使用</p>
              </div>
            </div>
            <div className="flex gap-3 items-start">
              <span className="text-purple-400 font-bold min-w-[24px]">④</span>
              <div>
                <p>クラウドサインから申込書を送仁E/p>
                <a href="https://app.cloudsign.jp/" target="_blank" rel="noopener noreferrer" className="text-xs text-blue-400 hover:underline">ↁEクラウドサインを開ぁE/a>
                <p className="text-xs text-slate-500 mt-0.5">顧客に電子署名してもらぁE/p>
              </div>
            </div>
            <div className="flex gap-3 items-start">
              <span className="text-purple-400 font-bold min-w-[24px]">⑤</span>
              <p>署名完亁E��確認したら「📁E連絡済みにする」�Eタンを押ぁE/p>
            </div>
          </div>
        </div>

        {/* STEP 3 シスチE��登録 */}
        <div className="mb-5 pl-4 border-l-2 border-blue-700">
          <p className="text-xs font-bold text-blue-400 uppercase tracking-wide mb-3">STEP 3 ── 保守シスチE��で更新登録</p>
          <div className="space-y-2 text-sm text-slate-300">
            {[
              { n:'①', t:'PayCube保守シスチE��にログイン', s:'https://dist.paycube-service.com/paycube/index.php (ID/PW: devicee)' },
              { n:'②', t:'「保守期限」から対象の設置先名をクリチE��' },
              { n:'③', t:'「登録」�Eタン ↁE保守サービス冁E��を�Eルダウンで選抁E },
              { n:'④', t:'「登録」�Eタンで完亁E },
            ].map(r => (
              <div key={r.n} className="flex gap-3 items-start">
                <span className="text-blue-400 font-bold min-w-[24px]">{r.n}</span>
                <div>
                  <p>{r.t}</p>
                  {r.s && <p className="text-xs text-slate-500 mt-0.5">{r.s}</p>}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* STEP 4 完亁E�E琁E*/}
        <div className="mb-5 pl-4 border-l-2 border-orange-700">
          <p className="text-xs font-bold text-orange-400 uppercase tracking-wide mb-3">STEP 4 ── 完亁E�E琁E��忁E��！E/p>
          <div className="space-y-2 text-sm text-slate-300">
            <div className="flex gap-3 items-start">
              <span className="text-orange-400 font-bold min-w-[24px]">①</span>
              <div>
                <p>進捗管琁E��ート�E <span className="font-bold text-white">K列まで</span> 入力すめE/p>
                <a href="https://docs.google.com/spreadsheets/d/107wEIMY-wiIcPg0K_cDfyVGajKoFmluto8wJdSbqeOg/edit?gid=849544635#gid=849544635" target="_blank" rel="noopener noreferrer" className="text-xs text-blue-400 hover:underline">ↁE進捗管琁E��ートを開く</a>
              </div>
            </div>
            <div className="flex gap-3 items-start">
              <span className="text-orange-400 font-bold min-w-[24px]">②</span>
              <p>野田さんへエスカレーション連絡</p>
            </div>
            <div className="flex gap-3 items-start">
              <span className="text-orange-400 font-bold min-w-[24px]">③</span>
              <p>こ�Eペ�Eジで「✅ 更新完亁E���Eタンを押してスチE�Eタスを更新</p>
            </div>
          </div>
        </div>

        {/* 例外フロー */}
        <div className="p-4 bg-red-950/50 border border-red-700 rounded-xl">
          <p className="font-bold text-red-300 mb-2">🔴 例外ケース ↁE吉井さんへ即エスカレーション</p>
          <ul className="text-sm text-slate-300 space-y-1">
            <li>• 保守期間が <span className="text-red-400 font-medium">すでに刁E��てぁE��</span> 状態での再加入依頼�E�シスチE��登録不可�E�E/li>
            <li>• 途中解紁E�E別プランへの刁E��替え希望</li>
            <li>• 上訁Eケースは自己判断せず忁E��吉井さんへ連絡すること</li>
          </ul>
        </div>
      </div>

      {/* 費用回収フロー */}
      <div className="mt-4 p-5 bg-slate-800 border border-slate-700 rounded-xl">
        <h3 className="font-bold text-white mb-4">💰 費用回収フロー�E�有償保守加入確定後！E/h3>
        <div className="space-y-3">
          {[
            { n:'1', icon:'📝', title:'見積書を作�E', desc:'フォーマット（見積書Excel�E�に記�E。�Eラン・金額�E見積期限を記載、E, note:'料��は税別。フォーマット�E野田さんから入扁E },
            { n:'2', icon:'✁E, title:'社長へ見積書の承認依頼', desc:'送付前に忁E��社長の承認を取る、E, note:'承認前に顧客へ送付しなぁE },
            { n:'3', icon:'📧', title:'顧客へ見積書を送仁E, desc:'メールに見積書PDFを添付して送付。同時に申込書�E�Eay Cube有償保守�Eラン申込書.xlsx�E��E記�E・返送を依頼、E, note:'急ぎ�E場合�E申込書回収を征E��ずに次のスチE��プへ�E�野田さんに確認！E },
            { n:'4', icon:'📄', title:'顧客から申込書を回叁E, desc:'記�E・押印済みの申込書をメールで受領。押印・署名�E顧客拁E��老E�Eも�EでOK、E, note:'' },
            { n:'5', icon:'🏦', title:'岡田さん�E�総務�E�へ請求書発行依頼', desc:'見積書・申込書・有償保守開始日・納品日を添えてメールで依頼。支払期日は月末�E�コンラチE��スへの入金に間に合わせる�E�、E, note:'支払期日は顧客に事前確認が忁E��E },
            { n:'6', icon:'📞', title:'コンラチE��ス吉井さんへ保守登録連絡', desc:'加入意思が確定したら吉井さん！E90-3567-7162�E�へ連絡し、保守登録を依頼、E, note:'⚠�E�E吉井さんが勝手に手続きを進めることがある。確認なしで進めさせなぁE },
            { n:'7', icon:'📊', title:'進捗管琁E��ートに記録', desc:'保守期間（開始日〜終亁E���E�をシートに記載。��額�EU列に記�E、E, note:'管琁E��ート�EU列が請求総顁E },
          ].map(r => (
            <div key={r.n} className="flex gap-3 items-start">
              <div className="w-7 h-7 rounded-full bg-blue-700 text-white text-xs font-bold flex items-center justify-center flex-shrink-0 mt-0.5">{r.n}</div>
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span>{r.icon}</span>
                  <p className="font-medium text-white text-sm">{r.title}</p>
                </div>
                <p className="text-sm text-slate-300 mt-0.5 ml-6">{r.desc}</p>
                {r.note && <p className="text-xs text-yellow-400 mt-0.5 ml-6">⚠�E�E{r.note}</p>}
              </div>
            </div>
          ))}
        </div>

        <div className="mt-5 grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div className="p-3 bg-slate-700/50 rounded-lg text-sm">
            <p className="text-xs font-bold text-slate-400 mb-2">📌 よく使ぁE��絡允E/p>
            <ul className="space-y-1 text-slate-300">
              <li>🏦 請求書発行：岡田さん�E�総務�E�E/li>
              <li>📞 保守登録�E�コンラチE��ス吉井さめE<span className="font-mono text-white">090-3567-7162</span></li>
              <li>✁E最終確認：野田さん</li>
            </ul>
          </div>
          <div className="p-3 bg-slate-700/50 rounded-lg text-sm">
            <p className="text-xs font-bold text-slate-400 mb-2">⚠�E�E注意事頁E/p>
            <ul className="space-y-1 text-slate-300 text-xs">
              <li>• 料��はすべて<span className="text-yellow-300 font-medium">税別</span></li>
              <li>• 吉井さんが確認なしで手続きを勝手に進める場合あめEↁE事前に釘を刺ぁE/li>
              <li>• コンラチE��スへの入金�E月末 ↁE請求書発行�E早めに</li>
              <li>• 愛真館は社長判断で請求保留中�E�米山さんへ確認！E/li>
            </ul>
          </div>
        </div>
      </div>

      {/* コンラチE��スからの請求構造 */}
      <div className="mt-4 p-5 bg-slate-800 border border-slate-700 rounded-xl">
        <h3 className="font-bold text-white mb-1">🧾 コンラチE��ス�E�仕�E�E�請求�E仕絁E��</h3>
        <p className="text-xs text-slate-500 mb-4">出典�E�E026年3月�E請求書�E�株式会社日本コンラチE��ス ↁEチE��イスエージェンシー�E�E/p>
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <p className="text-xs font-bold text-slate-400 mb-2">📌 請求フロー</p>
            <div className="space-y-2 text-sm text-slate-300">
              <div className="flex gap-2 items-center">
                <span className="px-2 py-0.5 bg-blue-800 text-blue-200 rounded text-xs">コンラチE��ス</span>
                <span className="text-slate-500">ↁE/span>
                <span className="px-2 py-0.5 bg-slate-600 text-slate-200 rounded text-xs">チE��イスエージェンシー</span>
                <span className="text-slate-500">ↁE/span>
                <span className="px-2 py-0.5 bg-green-800 text-green-200 rounded text-xs">顧客</span>
              </div>
              <p className="text-xs text-slate-400">コンラチE��スへの支払�E月末。顧客への請求�E月末を基本に先方と調整、E/p>
            </div>
            <div className="mt-3 space-y-1 text-xs text-slate-300">
              <p className="font-bold text-slate-400">振込先（コンラチE��ス�E�E/p>
              <p>三井住友銀衁E日比谷支庁E当座 6732482</p>
              <p>みずほ銀衁E芝支庁E当座 0104220</p>
              <p className="text-slate-500">口座名：株式会社日本コンラチE��ス</p>
            </div>
          </div>
          <div>
            <p className="text-xs font-bold text-slate-400 mb-2">💴 仕�E価格�E�コンラチE��スからの請求単価�E�E/p>
            <table className="w-full text-xs">
              <tbody className="divide-y divide-slate-700">
                {[
                  { plan: 'オンサイト＋部品代込パック�E�年間！E, price: '¥46,400' },
                ].map((r, i) => (
                  <tr key={i}>
                    <td className="py-1.5 text-slate-300">{r.plan}</td>
                    <td className="py-1.5 text-right font-mono font-bold text-white">{r.price}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p className="text-xs text-yellow-400 mt-2">⚠�E�E顧客への売値�E�¥81,600�E�と仕�E価格�E�¥46,400�E��E別。差額が利益、E/p>
          </div>
        </div>

        {/* 申込書重要事頁E*/}
        <div className="mt-4 p-3 bg-slate-700/50 rounded-lg">
          <p className="text-xs font-bold text-slate-300 mb-2">📋 申込書 重要事頁E��顧客への説明忁E��！E/p>
          <ul className="text-xs text-slate-400 space-y-1">
            <li>• 支払確認後に有償保守�Eランが適用�E�前払い�E�E/li>
            <li>• 契紁E��低期間�E<span className="text-white">1年閁E/span>。中途解紁E��も残期間�E料��が発甁E/li>
            <li>• 契紁E�E<span className="text-white">1年ごと自動更新</span>。翌年刁E�E更新日の1ヶ月前までに支払いが忁E��E/li>
            <li>• 解紁E�E次回更新日の<span className="text-white">3ヶ月前</span>までに連絡が忁E��E/li>
            <li>• 支払遅延の場合�Eサービスが一時停止される可能性あり</li>
            <li>• お問ぁE��わせ�E�TEL 050-3627-9865 / support@and-iot.jp</li>
          </ul>
        </div>
      </div>

      {/* 保守�Eラン料��表 */}
      <div className="mt-4 p-5 bg-slate-800 border border-slate-700 rounded-xl">
        <h3 className="font-bold text-white mb-1">💴 保守�Eラン料��表</h3>
        <p className="text-xs text-slate-500 mb-4">出典�E�PayCube保守対応�Eご提案（株式会社チE��イスエージェンシー�E�E/p>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-600">
                <th className="text-left py-2 px-3 text-slate-400 font-medium">プラン</th>
                <th className="text-right py-2 px-3 text-slate-400 font-medium">年払い料��</th>
                <th className="text-left py-2 px-3 text-slate-400 font-medium">備老E/th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700">
              {[
                { plan: 'コールセンター機�E', price: '¥28,800', note: '365日・24時間' },
                { plan: 'オンサイト保守機�E', price: '¥31,700', note: '365日・9時、E1晁E },
                { plan: '部品代込プラン�E�Eption�E�E, price: '¥24,000', note: '別途請求なし（電源�E基盤除く！E },
                { plan: 'コールセンター�E�オンサイチEset', price: '¥57,600', note: '¥2,900お征E },
                { plan: 'コールセンター�E�オンサイト＋部品代込 set', price: '¥81,600', note: '最も手厚いプラン' },
                { plan: '設置・取説 / 撤去', price: '¥61,200', note: '1件あたり�E平日9、E5晁E },
                { plan: 'スポット保宁E, price: '¥84,000、E, note: '平日9、E7時�E5営業日以冁E�E部品代別送E },
              ].map((r, i) => (
                <tr key={i} className="hover:bg-slate-700/40 transition-colors">
                  <td className="py-2.5 px-3 text-slate-200">{r.plan}</td>
                  <td className="py-2.5 px-3 text-right font-mono font-bold text-white">{r.price}</td>
                  <td className="py-2.5 px-3 text-slate-400 text-xs">{r.note}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-3">
          <div className="p-3 bg-slate-700/50 rounded-lg">
            <p className="text-xs font-bold text-slate-300 mb-2">📦 無償保守期閁E/p>
            <p className="text-sm text-slate-300">設置日また�E稼働日から <span className="text-white font-bold">6ヶ月間</span></p>
            <p className="text-xs text-slate-500 mt-1">オンサイト保守＋部品代 無儁E/p>
          </div>
          <div className="p-3 bg-slate-700/50 rounded-lg">
            <p className="text-xs font-bold text-slate-300 mb-2">⚠�E�E注意事頁E/p>
            <ul className="text-xs text-slate-400 space-y-1">
              <li>• 部品代込プランの対象外：電源�E本体基盤</li>
              <li>• 離島�E�別途交通費等が発甁E/li>
              <li>• 改造品�E仕様変更品�Eオンサイト除夁E/li>
            </ul>
          </div>
        </div>
      </div>

      {/* 更新案�EメールチE��プレート（有償保守！E*/}
      <RenewalMailTemplate />

      {/* 顧客送付メールチE��プレート（無償�E有償�E�E*/}
      <MailTemplate />
    </div>
  )
}

function MailTemplate() {
  const [copied, setCopied] = useState(false)
  const [company, setCompany] = useState('')
  const [contact, setContact] = useState('')
  const [myName, setMyName] = useState('')
  const [endDate, setEndDate] = useState('')
  const [startDate, setStartDate] = useState('')
  const [deadline, setDeadline] = useState('')

  const body = `、E{company || '会社名また�E物件吁E}、E、E{contact || 'ご担当老E��'}】槁E
ぁE��も大変お世話になっております、E株式会社チE��イスエージェンシーの${myName || '【�E刁E�E名前、E}でござぁE��す、E
標記�E件につきまして、ご連絡申し上げます、E現在ご利用ぁE��だぁE��おります現金精算機「PayCube」につきましては、無償保証期間ぁE{endDate || '【YYYY年M朁E日、E}をもって終亁E��たします、Eこれに伴ぁE��E{startDate || '【YYYY年M朁E日、E}より有償保守サービスへの移行となります、Eつきましては、有償保守サービスに関するお見積書を添付�Eとおり送付いたします�Eで、ご確認�Eほどお願い申し上げます、Eなお、近日中にクラウドサインよりお申込書をお送りぁE��します�Eで、併せて${deadline || '【YYYY年M朁E日、E}までにご対応賜りますよぁE��願い申し上げます、E
何卒よろしくお願い申し上げます、E
${myName || '【署名、E}
株式会社チE��イスエージェンシー`

  const copy = () => {
    navigator.clipboard.writeText(body)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="mt-4 p-5 bg-slate-800 border border-slate-700 rounded-xl">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-white">📧 顧客送付メールチE��プレーチE/h3>
        <div className="flex items-center gap-2 text-xs text-slate-400">
          <span>件名！E/span>
          <span className="text-slate-300 font-medium">現金精算機PayCube 有償保守サービスのお見積書送付�E件</span>
        </div>
      </div>

      {/* 入力フォーム */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4">
        {[
          { key: 'company',   label: '会社吁E物件吁E, val: company,   set: setCompany,   placeholder: '例：株式会社、E��E�EチE��' },
          { key: 'contact',   label: 'ご担当老E��',   val: contact,   set: setContact,   placeholder: '例：山田' },
          { key: 'myName',    label: '自刁E�E名前',   val: myName,    set: setMyName,    placeholder: '例：米山' },
          { key: 'endDate',   label: '無償保証終亁E��', val: endDate,  set: setEndDate,   placeholder: '例！E026年9朁E0日' },
          { key: 'startDate', label: '有償保守開始日', val: startDate,set: setStartDate, placeholder: '例！E026年10朁E日' },
          { key: 'deadline',  label: '申込期限',     val: deadline,  set: setDeadline,  placeholder: '例！E026年9朁E0日' },
        ].map(({ key, label, val, set, placeholder }) => (
          <div key={key}>
            <label className="text-xs text-slate-400 mb-1 block">{label}</label>
            <input
              type="text"
              value={val}
              placeholder={placeholder}
              onChange={e => set(e.target.value)}
              className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:border-blue-500 focus:outline-none"
            />
          </div>
        ))}
      </div>

      {/* プレビュー */}
      <div className="relative">
        <pre className="w-full p-4 bg-slate-900 border border-slate-600 rounded-lg text-sm text-slate-200 whitespace-pre-wrap font-sans leading-relaxed">{body}</pre>
        <button
          onClick={copy}
          className={`absolute top-3 right-3 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${copied ? 'bg-green-600 text-white' : 'bg-slate-600 hover:bg-slate-500 text-white'}`}
        >
          {copied ? '✁Eコピ�E済み' : '📋 コピ�E'}
        </button>
      </div>
      <p className="text-xs text-slate-500 mt-2">※ 添付ファイル�E�御見積書PDF�E�別途作�E�E�！E冁E��は自由にアレンジ可</p>
    </div>
  )
}

function RenewalMailTemplate() {
  const [copied, setCopied] = useState(false)
  const [company, setCompany] = useState('')
  const [contact, setContact] = useState('')
  const [myName, setMyName] = useState('')
  const [endDate, setEndDate] = useState('')
  const [planName, setPlanName] = useState('コールセンター�E�オンサイト＋部品代込プラン')
  const [deadline, setDeadline] = useState('')

  const body = `${company || '【会社吁E物件名、E}
${contact || '【ご拁E��老E��、E}槁E
ぁE��も大変お世話になっております、E株式会社チE��イスエージェンシーの${myName || '【�E刁E�E名前、E}でござぁE��す、E
標記�E件につきまして、ご連絡申し上げます、E現在ご契紁E��ただぁE��おります現金精算機「PayCube」�E
保守サービス�E�E{planName}�E�が
${endDate || '【YYYY年M朁E日、E}をもちまして契紁E��間満亁E��なります、E
つきましては、引き続き同�Eランにての更新をご案�E申し上げます、E
■ 保守サービスにご加入ぁE��だくメリチE��

【対応スピ�Eド、E保守契紁E��なぁE��合、故障時は「スポット対応」となり、Eご対応まで最大5営業日のお時間をぁE��だくことになります、E保守契紁E��ご加入ぁE��だくことで、E65日・9時、E1時�E
優先対応が可能となります、E
【費用リスクの軽減、E保守契紁E��しで敁E��した場合、修琁E��・部品代・出張費ぁE都度発生し、E回�E修琁E��数丁E��数十丁E�Eになるケースもございます、E�E�例：紙幣払�E機�E交揁E¥120,000 / 硬貨入金部モジュール ¥96,000�E�E保守契紁E��部品代込プラン�E�にご加入ぁE��だくと、Eこれら�E部品代が定額�Eに含まれます、E
【コールセンター対応、E365日・24時間のコールセンターにより、夜間・休日の
トラブル時もすぐにご相諁E��ただけます、E
ご不�Eな点めE��変更のご希望がございましたら、E${deadline || '【YYYY年M朁E日、E}までにご連絡賜りますよぁE��願い申し上げます、E
何卒よろしくお願い申し上げます、E
${myName || '【署名、E}
株式会社チE��イスエージェンシー`

  const copy = () => {
    navigator.clipboard.writeText(body)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="mt-4 p-5 bg-slate-800 border border-slate-700 rounded-xl">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-white">🔄 更新案�EメールチE��プレート（有償保守！E/h3>
        <div className="flex items-center gap-2 text-xs text-slate-400">
          <span>件名！E/span>
          <span className="text-slate-300 font-medium">現金精算機PayCube 保守サービス更新のご案�E</span>
        </div>
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4">
        {[
          { label: '会社吁E物件吁E, val: company,   set: setCompany,   placeholder: '例：ガーランドコート宁E��羁E },
          { label: 'ご担当老E��',   val: contact,   set: setContact,   placeholder: '例：山田' },
          { label: '自刁E�E名前',   val: myName,    set: setMyName,    placeholder: '例：米山' },
          { label: '保守終亁E��',   val: endDate,   set: setEndDate,   placeholder: '例！E026年8朁E9日' },
          { label: '現在のプラン', val: planName,  set: setPlanName,  placeholder: '例：コールセンター�E�オンサイト＋部品代込プラン' },
          { label: '返信期限',     val: deadline,  set: setDeadline,  placeholder: '例！E026年8朁E8日' },
        ].map(({ label, val, set, placeholder }) => (
          <div key={label}>
            <label className="text-xs text-slate-400 mb-1 block">{label}</label>
            <input
              type="text"
              value={val}
              placeholder={placeholder}
              onChange={e => set(e.target.value)}
              className="w-full px-3 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white text-sm focus:border-blue-500 focus:outline-none"
            />
          </div>
        ))}
      </div>
      <div className="relative">
        <pre className="w-full p-4 bg-slate-900 border border-slate-600 rounded-lg text-sm text-slate-200 whitespace-pre-wrap font-sans leading-relaxed">{body}</pre>
        <button
          onClick={copy}
          className={`absolute top-3 right-3 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${copied ? 'bg-green-600 text-white' : 'bg-slate-600 hover:bg-slate-500 text-white'}`}
        >
          {copied ? '✁Eコピ�E済み' : '📋 コピ�E'}
        </button>
      </div>
    </div>
  )
}
