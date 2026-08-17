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

      {/* 関連リンク */}
      <div className="mt-8 grid grid-cols-1 sm:grid-cols-2 gap-3">
        {[
          { label: 'PayCube保守システム（ログイン）', url: 'https://dist.paycube-service.com/paycube/customer_detail.php', icon: '🔐', desc: 'ID/PW: devicee' },
          { label: '進捗管理シート', url: 'https://docs.google.com/spreadsheets/d/107wEIMY-wiIcPg0K_cDfyVGajKoFmluto8wJdSbqeOg/edit?gid=849544635#gid=849544635', icon: '📊', desc: 'K列まで入力 → 野田さんへ連絡' },
          { label: 'PayCube保守マニュアル', url: '/manuals', icon: '📋', desc: '操作手順・エスカレーション基準' },
          { label: 'MailDealer（メール対応）', url: 'https://mdjack.maildealer.jp/index.php', icon: '📨', desc: '顧客への連絡はこちらから' },
          { label: 'Zoom Phone（架電）', url: 'https://app.zoom.us/wc/phone', icon: '📞', desc: '無償→有償切替の顧客連絡' },
          { label: 'くじらCRM', url: 'https://d1zlma8f7wwwsg.cloudfront.net/login', icon: '🐋', desc: '顧客情報の確認' },
          { label: '工程管理シート', url: 'https://docs.google.com/spreadsheets/d/1GiEvK-KLB7rl1lrCn-Llgl9H6W4m2PuZJXby2RqIuMc/edit?gid=602309486#gid=602309486', icon: '📈', desc: '全体進捗の管理' },
          { label: 'くじら社内Wiki', url: 'https://www.notion.so/kujira-device-agency/Wiki-dc27874409f24d549bb439103f852185', icon: '📖', desc: 'Notion Wiki' },
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
            <span className="text-slate-500 text-xs">↗</span>
          </a>
        ))}
      </div>

      {/* ログイン情報 */}
      <div className="mt-4 p-5 bg-slate-800 border border-slate-700 rounded-xl">
        <h3 className="font-bold text-white mb-3">🔐 保守システム ログイン情報</h3>
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
            <p className="text-slate-400 text-xs mb-1">パスワード</p>
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
              'ログイン後、画面下部「保守期限」セクションを確認',
              '「今月」「来月」「再来月」の3タブを全部チェック（漏れ防止）',
              '設置先名（青文字リンク）をクリック',
              '右側「登録」ボタンをクリック',
              '「保守サービス内容」プルダウンでプランを選択',
              '「登録」ボタンで完了',
              '進捗管理シートのK列まで入力',
              '野田さんへ連絡',
            ].map((step, i) => (
              <li key={i} className="flex gap-2">
                <span className="text-blue-400 font-bold min-w-[20px]">{i + 1}.</span>
                <span>{step}</span>
              </li>
            ))}
          </ol>
          <div className="mt-4 space-y-2">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-wide">プラン別対応</p>
            <div className="flex gap-2 text-xs">
              <span className="px-2 py-1 bg-green-900 text-green-200 rounded">有償保守</span>
              <span className="text-slate-400">顧客連絡不要 → 同プランで期間延長</span>
            </div>
            <div className="flex gap-2 text-xs">
              <span className="px-2 py-1 bg-purple-900 text-purple-200 rounded">無償保守</span>
              <span className="text-slate-400">顧客連絡必須 → 加入意思・希望プランを確認してから登録</span>
            </div>
          </div>
        </div>

        <div className="p-5 bg-slate-800 border border-green-800 rounded-xl">
          <h3 className="font-bold text-white mb-3">➕ 新規登録フロー</h3>
          <ol className="space-y-2 text-sm text-slate-300">
            {[
              'メニューから「新規登録」を選択',
              '不明な項目は進捗管理シートを参照して補完',
              '必須項目を入力（赤マーク付き）',
              '「保守申請に進む」をクリック',
              '無償保守はそのまま「申請」ボタンで完了',
              '進捗管理シートK列まで入力',
              '野田さんへ連絡',
            ].map((step, i) => (
              <li key={i} className="flex gap-2">
                <span className="text-green-400 font-bold min-w-[20px]">{i + 1}.</span>
                <span>{step}</span>
              </li>
            ))}
          </ol>
          <div className="mt-4 p-3 bg-yellow-900/40 border border-yellow-700 rounded-lg text-xs text-yellow-200">
            ⚠️ シリアルNo.不明の場合は <span className="font-mono font-bold">999999999</span>（9桁）を入力
          </div>
        </div>
      </div>

      {/* エスカレーション */}
      <div className="mt-4 p-5 bg-slate-800 border border-slate-700 rounded-xl">
        <h3 className="font-bold text-white mb-3">🚨 エスカレーション基準</h3>
        <div className="space-y-2 text-sm">
          <div className="flex items-start gap-3 p-3 bg-red-950/50 border border-red-800 rounded-lg">
            <span>🔴</span>
            <div><p className="text-red-300 font-medium">保守期間が切れた状態での再加入</p><p className="text-slate-400 text-xs mt-0.5">システム登録不可 → 直ちに吉井さんへエスカレーション</p></div>
          </div>
          <div className="flex items-start gap-3 p-3 bg-yellow-950/50 border border-yellow-800 rounded-lg">
            <span>🟡</span>
            <div><p className="text-yellow-300 font-medium">保守の途中解約・別プランへの切り替え</p><p className="text-slate-400 text-xs mt-0.5">自己判断せず → 吉井さんへエスカレーション</p></div>
          </div>
          <div className="flex items-start gap-3 p-3 bg-green-950/50 border border-green-800 rounded-lg">
            <span>✅</span>
            <div><p className="text-green-300 font-medium">通常の更新・新規登録</p><p className="text-slate-400 text-xs mt-0.5">進捗管理シート記入 → 野田さんへ連絡</p></div>
          </div>
        </div>
      </div>
      {/* アラート発生時の対応フロー */}
      <div className="mt-4 p-5 bg-slate-800 border border-slate-700 rounded-xl">
        <h3 className="font-bold text-white mb-4">🚨 アラート発生時の対応フロー</h3>

        {/* 現在のプラン分岐 */}
        <div className="mb-5">
          <p className="text-xs font-bold text-slate-400 uppercase tracking-wide mb-3">STEP 1 ── 現在のプランを確認する</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div className="p-4 bg-green-950/50 border border-green-700 rounded-xl">
              <p className="font-bold text-green-300 mb-2">✅ 有償保守の場合</p>
              <ul className="text-sm text-slate-300 space-y-1">
                <li>→ 顧客への連絡 <span className="text-green-400 font-medium">不要</span></li>
                <li>→ 同プランで期間延長して登録するだけ</li>
                <li className="text-slate-500 text-xs mt-1">※ STEP 3（システム登録）へ進む</li>
              </ul>
            </div>
            <div className="p-4 bg-purple-950/50 border border-purple-700 rounded-xl">
              <p className="font-bold text-purple-300 mb-2">⚠️ 無償保守の場合</p>
              <ul className="text-sm text-slate-300 space-y-1">
                <li>→ 顧客への連絡 <span className="text-red-400 font-medium">必須</span></li>
                <li>→ 加入意思と希望プランを確認してから登録</li>
                <li className="text-slate-500 text-xs mt-1">※ STEP 2（顧客連絡）へ進む</li>
              </ul>
            </div>
          </div>
        </div>

        {/* STEP 2 無償保守のみ */}
        <div className="mb-5 pl-4 border-l-2 border-purple-700">
          <p className="text-xs font-bold text-purple-400 uppercase tracking-wide mb-3">STEP 2 ── 顧客へ連絡（無償保守のみ）</p>
          <div className="space-y-2 text-sm text-slate-300">
            <div className="flex gap-3 items-start">
              <span className="text-purple-400 font-bold min-w-[24px]">①</span>
              <div>
                <p>MailDealer or Zoom Phone で顧客へ連絡</p>
                <p className="text-xs text-slate-500 mt-0.5">「無償保証期間が〇月〇日に終了します。有償保守への移行についてご案内いたします」</p>
              </div>
            </div>
            <div className="flex gap-3 items-start">
              <span className="text-purple-400 font-bold min-w-[24px]">②</span>
              <div>
                <p>希望プランの確認（下記料金表を参考に案内）</p>
                <p className="text-xs text-slate-500 mt-0.5">コールセンターのみ ¥28,800 / オンサイト込 ¥57,600 / 全部入り ¥81,600</p>
              </div>
            </div>
            <div className="flex gap-3 items-start">
              <span className="text-purple-400 font-bold min-w-[24px]">③</span>
              <div>
                <p>見積書PDFを添付してメール送付</p>
                <p className="text-xs text-slate-500 mt-0.5">↓ 下のメールテンプレートを使用</p>
              </div>
            </div>
            <div className="flex gap-3 items-start">
              <span className="text-purple-400 font-bold min-w-[24px]">④</span>
              <div>
                <p>クラウドサインから申込書を送付</p>
                <a href="https://app.cloudsign.jp/" target="_blank" rel="noopener noreferrer" className="text-xs text-blue-400 hover:underline">→ クラウドサインを開く</a>
                <p className="text-xs text-slate-500 mt-0.5">顧客に電子署名してもらう</p>
              </div>
            </div>
            <div className="flex gap-3 items-start">
              <span className="text-purple-400 font-bold min-w-[24px]">⑤</span>
              <p>署名完了を確認したら「📞 連絡済みにする」ボタンを押す</p>
            </div>
          </div>
        </div>

        {/* STEP 3 システム登録 */}
        <div className="mb-5 pl-4 border-l-2 border-blue-700">
          <p className="text-xs font-bold text-blue-400 uppercase tracking-wide mb-3">STEP 3 ── 保守システムで更新登録</p>
          <div className="space-y-2 text-sm text-slate-300">
            {[
              { n:'①', t:'PayCube保守システムにログイン', s:'https://dist.paycube-service.com/paycube/index.php (ID/PW: devicee)' },
              { n:'②', t:'「保守期限」から対象の設置先名をクリック' },
              { n:'③', t:'「登録」ボタン → 保守サービス内容をプルダウンで選択' },
              { n:'④', t:'「登録」ボタンで完了' },
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

        {/* STEP 4 完了処理 */}
        <div className="mb-5 pl-4 border-l-2 border-orange-700">
          <p className="text-xs font-bold text-orange-400 uppercase tracking-wide mb-3">STEP 4 ── 完了処理（必須）</p>
          <div className="space-y-2 text-sm text-slate-300">
            <div className="flex gap-3 items-start">
              <span className="text-orange-400 font-bold min-w-[24px]">①</span>
              <div>
                <p>進捗管理シートの <span className="font-bold text-white">K列まで</span> 入力する</p>
                <a href="https://docs.google.com/spreadsheets/d/107wEIMY-wiIcPg0K_cDfyVGajKoFmluto8wJdSbqeOg/edit?gid=849544635#gid=849544635" target="_blank" rel="noopener noreferrer" className="text-xs text-blue-400 hover:underline">→ 進捗管理シートを開く</a>
              </div>
            </div>
            <div className="flex gap-3 items-start">
              <span className="text-orange-400 font-bold min-w-[24px]">②</span>
              <p>野田さんへエスカレーション連絡</p>
            </div>
            <div className="flex gap-3 items-start">
              <span className="text-orange-400 font-bold min-w-[24px]">③</span>
              <p>このページで「✅ 更新完了」ボタンを押してステータスを更新</p>
            </div>
          </div>
        </div>

        {/* 例外フロー */}
        <div className="p-4 bg-red-950/50 border border-red-700 rounded-xl">
          <p className="font-bold text-red-300 mb-2">🔴 例外ケース → 吉井さんへ即エスカレーション</p>
          <ul className="text-sm text-slate-300 space-y-1">
            <li>• 保守期間が <span className="text-red-400 font-medium">すでに切れている</span> 状態での再加入依頼（システム登録不可）</li>
            <li>• 途中解約・別プランへの切り替え希望</li>
            <li>• 上記2ケースは自己判断せず必ず吉井さんへ連絡すること</li>
          </ul>
        </div>
      </div>

      {/* 保守プラン料金表 */}
      <div className="mt-4 p-5 bg-slate-800 border border-slate-700 rounded-xl">
        <h3 className="font-bold text-white mb-1">💴 保守プラン料金表</h3>
        <p className="text-xs text-slate-500 mb-4">出典：PayCube保守対応のご提案（株式会社デバイスエージェンシー）</p>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="border-b border-slate-600">
                <th className="text-left py-2 px-3 text-slate-400 font-medium">プラン</th>
                <th className="text-right py-2 px-3 text-slate-400 font-medium">年払い料金</th>
                <th className="text-left py-2 px-3 text-slate-400 font-medium">備考</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700">
              {[
                { plan: 'コールセンター機能', price: '¥28,800', note: '365日・24時間' },
                { plan: 'オンサイト保守機能', price: '¥31,700', note: '365日・9時〜21時' },
                { plan: '部品代込プラン（Option）', price: '¥24,000', note: '別途請求なし（電源・基盤除く）' },
                { plan: 'コールセンター＋オンサイト set', price: '¥57,600', note: '¥2,900お得' },
                { plan: 'コールセンター＋オンサイト＋部品代込 set', price: '¥81,600', note: '最も手厚いプラン' },
                { plan: '設置・取説 / 撤去', price: '¥61,200', note: '1件あたり・平日9〜15時' },
                { plan: 'スポット保守', price: '¥84,000〜', note: '平日9〜17時・5営業日以内・部品代別途' },
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
            <p className="text-xs font-bold text-slate-300 mb-2">📦 無償保守期間</p>
            <p className="text-sm text-slate-300">設置日または稼働日から <span className="text-white font-bold">6ヶ月間</span></p>
            <p className="text-xs text-slate-500 mt-1">オンサイト保守＋部品代 無償</p>
          </div>
          <div className="p-3 bg-slate-700/50 rounded-lg">
            <p className="text-xs font-bold text-slate-300 mb-2">⚠️ 注意事項</p>
            <ul className="text-xs text-slate-400 space-y-1">
              <li>• 部品代込プランの対象外：電源・本体基盤</li>
              <li>• 離島：別途交通費等が発生</li>
              <li>• 改造品・仕様変更品はオンサイト除外</li>
            </ul>
          </div>
        </div>
      </div>

      {/* 更新案内メールテンプレート（有償保守） */}
      <RenewalMailTemplate />

      {/* 顧客送付メールテンプレート（無償→有償） */}
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

  const body = `【${company || '会社名または物件名'}】
【${contact || 'ご担当者名'}】様

いつも大変お世話になっております。
株式会社デバイスエージェンシーの${myName || '【自分の名前】'}でございます。

標記の件につきまして、ご連絡申し上げます。
現在ご利用いただいております現金精算機「PayCube」につきましては、無償保証期間が${endDate || '【YYYY年M月D日】'}をもって終了いたします。
これに伴い、${startDate || '【YYYY年M月D日】'}より有償保守サービスへの移行となります。
つきましては、有償保守サービスに関するお見積書を添付のとおり送付いたしますので、ご確認のほどお願い申し上げます。
なお、近日中にクラウドサインよりお申込書をお送りいたしますので、併せて${deadline || '【YYYY年M月D日】'}までにご対応賜りますようお願い申し上げます。

何卒よろしくお願い申し上げます。

${myName || '【署名】'}
株式会社デバイスエージェンシー`

  const copy = () => {
    navigator.clipboard.writeText(body)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="mt-4 p-5 bg-slate-800 border border-slate-700 rounded-xl">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-white">📧 顧客送付メールテンプレート</h3>
        <div className="flex items-center gap-2 text-xs text-slate-400">
          <span>件名：</span>
          <span className="text-slate-300 font-medium">現金精算機PayCube 有償保守サービスのお見積書送付の件</span>
        </div>
      </div>

      {/* 入力フォーム */}
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4">
        {[
          { key: 'company',   label: '会社名/物件名', val: company,   set: setCompany,   placeholder: '例：株式会社〇〇ホテル' },
          { key: 'contact',   label: 'ご担当者名',   val: contact,   set: setContact,   placeholder: '例：山田' },
          { key: 'myName',    label: '自分の名前',   val: myName,    set: setMyName,    placeholder: '例：米山' },
          { key: 'endDate',   label: '無償保証終了日', val: endDate,  set: setEndDate,   placeholder: '例：2026年9月30日' },
          { key: 'startDate', label: '有償保守開始日', val: startDate,set: setStartDate, placeholder: '例：2026年10月1日' },
          { key: 'deadline',  label: '申込期限',     val: deadline,  set: setDeadline,  placeholder: '例：2026年9月20日' },
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
          {copied ? '✅ コピー済み' : '📋 コピー'}
        </button>
      </div>
      <p className="text-xs text-slate-500 mt-2">※ 添付ファイル：御見積書PDF（別途作成）／ 内容は自由にアレンジ可</p>
    </div>
  )
}

function RenewalMailTemplate() {
  const [copied, setCopied] = useState(false)
  const [company, setCompany] = useState('')
  const [contact, setContact] = useState('')
  const [myName, setMyName] = useState('')
  const [endDate, setEndDate] = useState('')
  const [planName, setPlanName] = useState('コールセンター＋オンサイト＋部品代込プラン')
  const [deadline, setDeadline] = useState('')

  const body = `${company || '【会社名/物件名】'}
${contact || '【ご担当者名】'}様

いつも大変お世話になっております。
株式会社デバイスエージェンシーの${myName || '【自分の名前】'}でございます。

標記の件につきまして、ご連絡申し上げます。
現在ご契約いただいております現金精算機「PayCube」の
保守サービス（${planName}）が
${endDate || '【YYYY年M月D日】'}をもちまして契約期間満了となります。

つきましては、引き続き同プランにての更新をご案内申し上げます。

■ 保守サービスにご加入いただくメリット

【対応スピード】
保守契約がない場合、故障時は「スポット対応」となり、
ご対応まで最大5営業日のお時間をいただくことになります。
保守契約にご加入いただくことで、365日・9時〜21時の
優先対応が可能となります。

【費用リスクの軽減】
保守契約なしで故障した場合、修理費・部品代・出張費が
都度発生し、1回の修理で数万〜数十万円になるケースもございます。
（例：紙幣払出機の交換 ¥120,000 / 硬貨入金部モジュール ¥96,000）
保守契約（部品代込プラン）にご加入いただくと、
これらの部品代が定額内に含まれます。

【コールセンター対応】
365日・24時間のコールセンターにより、夜間・休日の
トラブル時もすぐにご相談いただけます。

ご不明な点やご変更のご希望がございましたら、
${deadline || '【YYYY年M月D日】'}までにご連絡賜りますようお願い申し上げます。

何卒よろしくお願い申し上げます。

${myName || '【署名】'}
株式会社デバイスエージェンシー`

  const copy = () => {
    navigator.clipboard.writeText(body)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  return (
    <div className="mt-4 p-5 bg-slate-800 border border-slate-700 rounded-xl">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-bold text-white">🔄 更新案内メールテンプレート（有償保守）</h3>
        <div className="flex items-center gap-2 text-xs text-slate-400">
          <span>件名：</span>
          <span className="text-slate-300 font-medium">現金精算機PayCube 保守サービス更新のご案内</span>
        </div>
      </div>
      <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 mb-4">
        {[
          { label: '会社名/物件名', val: company,   set: setCompany,   placeholder: '例：ガーランドコート宇佐美' },
          { label: 'ご担当者名',   val: contact,   set: setContact,   placeholder: '例：山田' },
          { label: '自分の名前',   val: myName,    set: setMyName,    placeholder: '例：米山' },
          { label: '保守終了日',   val: endDate,   set: setEndDate,   placeholder: '例：2026年8月19日' },
          { label: '現在のプラン', val: planName,  set: setPlanName,  placeholder: '例：コールセンター＋オンサイト＋部品代込プラン' },
          { label: '返信期限',     val: deadline,  set: setDeadline,  placeholder: '例：2026年8月18日' },
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
          {copied ? '✅ コピー済み' : '📋 コピー'}
        </button>
      </div>
    </div>
  )
}
