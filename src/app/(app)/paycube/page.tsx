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
  urgent:   { bg: 'bg-orange-950/60', border: 'border-orange-500', badge: 'bg-orange-500 text-white', label: '🟠 要対応', icon: '⚠️' },
  warning:  { bg: 'bg-yellow-950/60', border: 'border-yellow-500', badge: 'bg-yellow-600 text-white', label: '🟡 注意', icon: '📋' },
  ok:       { bg: 'bg-slate-800', border: 'border-slate-700', badge: 'bg-slate-600 text-slate-200', label: '✅ 余裕あり', icon: '✅' },
}

const statusLabel: Record<string, string> = {
  active: '未対応',
  alerted: '⚠️ アラート済',
  contacted: '📞 連絡済',
  renewed: '✅ 更新完了',
  expired: '❌ 期限切れ',
}

export default function PayCubePage() {
  const [contracts, setContracts] = useState<Contract[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'alert' | 'all'>('alert')
  const [updating, setUpdating] = useState<string | null>(null)
  const [showAdd, setShowAdd] = useState(false)
  const [form, setForm] = useState({
    client_name: '', management_no: '', plan_name: '', plan_type: 'paid',
    start_date: '', end_date: '', notes: '', product_type: '',
    serial_no_hard: '', serial_no_bill: ''
  })

  const load = async () => {
    setLoading(true)
    const res = await fetch(`/api/paycube/contracts${filter === 'alert' ? '?mode=alert' : ''}`)
    const d = await res.json()
    setContracts(d.contracts || [])
    setLoading(false)
  }

  useEffect(() => { load() }, [filter])

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
    if (!form.client_name || !form.end_date) return alert('設置先名と保守終了日は必須です')
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
        <h1 className="text-2xl font-bold text-white">🔔 PayCube保守期限アラート</h1>
        <p className="text-slate-400 text-sm mt-1">2ヶ月前から自動アラート。期限切れ前に顧客連絡・更新手続きを完了してください。</p>
      </div>

      {/* アラートサマリーバナー */}
      {(critical.length > 0 || urgent.length > 0 || warning.length > 0) && filter === 'alert' && (
        <div className="mb-6 space-y-3">
          {critical.length > 0 && (
            <div className="flex items-center gap-3 px-5 py-4 bg-red-900/80 border border-red-500 rounded-xl animate-pulse">
              <span className="text-2xl">🚨</span>
              <div>
                <p className="font-bold text-red-200 text-lg">緊急！{critical.length}件が2週間以内に期限切れ</p>
                <p className="text-red-300 text-sm">即座に顧客連絡・保守システムへの更新登録が必要です</p>
              </div>
            </div>
          )}
          {urgent.length > 0 && (
            <div className="flex items-center gap-3 px-5 py-4 bg-orange-900/60 border border-orange-500 rounded-xl">
              <span className="text-2xl">⚠️</span>
              <div>
                <p className="font-bold text-orange-200">{urgent.length}件が1ヶ月以内に期限切れ</p>
                <p className="text-orange-300 text-sm">顧客への連絡を開始してください</p>
              </div>
            </div>
          )}
          {warning.length > 0 && (
            <div className="flex items-center gap-3 px-5 py-4 bg-yellow-900/40 border border-yellow-600 rounded-xl">
              <span className="text-2xl">📋</span>
              <div>
                <p className="font-bold text-yellow-200">{warning.length}件が2ヶ月以内に期限切れ</p>
                <p className="text-yellow-300 text-sm">準備を進めてください（無償保守の場合は顧客確認が必要）</p>
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
          onClick={() => setFilter('all')}
          className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${filter === 'all' ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}
        >
          📋 全件表示
        </button>
        <button
          onClick={() => fetch('/api/paycube/check-alerts').then(() => load())}
          className="px-4 py-2 rounded-lg text-sm font-medium bg-slate-700 text-slate-300 hover:bg-slate-600 transition-colors"
        >
          🔄 手動チェック実行
        </button>
        <button
          onClick={() => setShowAdd(!showAdd)}
          className="px-4 py-2 rounded-lg text-sm font-medium bg-green-700 text-white hover:bg-green-600 transition-colors ml-auto"
        >
          ＋ 契約登録
        </button>
      </div>

      {/* 新規登録フォーム */}
      {showAdd && (
        <div className="mb-6 p-5 bg-slate-800 border border-slate-600 rounded-xl">
          <h2 className="font-bold text-white mb-4">📝 PayCube契約登録</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {[
              { key: 'client_name', label: '設置先名 *', type: 'text', required: true },
              { key: 'management_no', label: '管理番号(コンラックス)', type: 'text' },
              { key: 'product_type', label: '製品タイプ', type: 'text', placeholder: 'キュービック型(黒)' },
              { key: 'plan_name', label: '保守サービス内容', type: 'text', placeholder: '1年目:コールセンター利用' },
              { key: 'start_date', label: '保守開始日', type: 'date' },
              { key: 'end_date', label: '保守終了日 *', type: 'date', required: true },
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
                <option value="paid">有償保守</option>
                <option value="free">無償保守</option>
              </select>
            </div>
            <div>
              <label className="text-xs text-slate-400 mb-1 block">備考</label>
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

      {/* 契約一覧 */}
      {loading ? (
        <div className="text-slate-400 text-center py-12">読み込み中...</div>
      ) : contracts.length === 0 ? (
        <div className="text-slate-400 text-center py-12">
          <p className="text-4xl mb-3">✅</p>
          <p>アラート対象の契約はありません</p>
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
                        <span className="text-xs px-2 py-0.5 rounded-full bg-purple-700 text-purple-100 font-medium">無償保守⚠要確認</span>
                      )}
                      <span className="text-xs px-2 py-0.5 rounded-full bg-slate-600 text-slate-200">{statusLabel[c.status] || c.status}</span>
                    </div>
                    <div className="text-sm text-slate-300 space-y-0.5">
                      <p>📅 保守終了日: <span className={`font-bold ${level === 'critical' ? 'text-red-300' : level === 'urgent' ? 'text-orange-300' : level === 'warning' ? 'text-yellow-300' : 'text-white'}`}>{c.end_date}</span> <span className="text-slate-400">(残 {days}日)</span></p>
                      {c.plan_name && <p>📋 プラン: {c.plan_name}</p>}
                      {c.management_no && <p>🔢 管理番号: {c.management_no}</p>}
                      {c.contacted_at && <p>📞 連絡済: {new Date(c.contacted_at).toLocaleDateString('ja-JP')}</p>}
                      {c.notes && <p className="text-slate-400">📝 {c.notes}</p>}
                    </div>
                  </div>
                  {/* アクションボタン */}
                  <div className="flex flex-col gap-2 min-w-fit">
                    {c.status !== 'contacted' && c.status !== 'renewed' && (
                      <button
                        disabled={updating === c.id}
                        onClick={() => updateStatus(c.id, 'contacted')}
                        className="px-3 py-1.5 bg-blue-700 hover:bg-blue-600 text-white text-xs rounded-lg font-medium transition-colors whitespace-nowrap"
                      >
                        📞 連絡済みにする
                      </button>
                    )}
                    {c.status !== 'renewed' && (
                      <button
                        disabled={updating === c.id}
                        onClick={() => updateStatus(c.id, 'renewed')}
                        className="px-3 py-1.5 bg-green-700 hover:bg-green-600 text-white text-xs rounded-lg font-medium transition-colors whitespace-nowrap"
                      >
                        ✅ 更新完了
                      </button>
                    )}
                    <a
                      href="https://dist.paycube-service.com/paycube/customer_detail.php"
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-3 py-1.5 bg-slate-600 hover:bg-slate-500 text-white text-xs rounded-lg font-medium transition-colors text-center whitespace-nowrap"
                    >
                      🔗 保守システム
                    </a>
                  </div>
                </div>
              </div>
            )
          })}
        </div>
      )}

      {/* 操作ガイド */}
      <div className="mt-8 p-5 bg-slate-800 border border-slate-700 rounded-xl">
        <h3 className="font-bold text-white mb-3">📖 対応ガイド</h3>
        <div className="space-y-2 text-sm text-slate-300">
          <p>🔴 <strong className="text-red-300">緊急（2週間以内）</strong>：即座に顧客へ連絡 → 保守システムで更新登録 → 進捗シートK列入力 → 野田さんへ連絡</p>
          <p>🟠 <strong className="text-orange-300">要対応（1ヶ月以内）</strong>：顧客へ連絡開始。無償保守は加入意思・希望プランを確認してから登録</p>
          <p>🟡 <strong className="text-yellow-300">注意（2ヶ月以内）</strong>：準備開始。有償保守は同プランで延長、無償保守は顧客確認が必要</p>
          <p>⚠️ 期限切れ後の<strong>再加入はシステム登録不可</strong> → 吉井さんへエスカレーション</p>
          <p>📋 <a href="/manuals" className="text-blue-400 hover:underline">操作マニュアル詳細はこちら</a></p>
        </div>
      </div>
    </div>
  )
}
