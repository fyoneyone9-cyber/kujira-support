'use client'
import { useState, useCallback } from 'react'

// ── 切り返しデータ ──
const OBJECTION_TREE: Record<string, { label: string; response: string }> = {
  // カテゴリ
  'cat_busy':        { label: '⏰ 今は忙しい', response: '' },
  'cat_nointerest':  { label: '🚫 興味がない', response: '' },
  'cat_other':       { label: '🔀 他社を使っている', response: '' },
  'cat_price':       { label: '💰 高そう・費用がかかる', response: '' },
  'cat_timing':      { label: '📅 今は時期が悪い', response: '' },
  'cat_info':        { label: '📋 資料だけ欲しい', response: '' },
  // 忙しい系
  'busy_later':      { label: '後でかけ直して', response: '「承知しました。改めてご連絡します。よろしければメールでも資料をお送りできますが、アドレスをいただけますか？」' },
  'busy_now':        { label: '今は対応できない', response: '「お忙しいところ失礼しました。IT補助金の申請期限が近づいておりまして、2分だけいただけますか？」' },
  // 興味なし系
  'nointerest_already': { label: 'もう検討してない', response: '「そうですか。実は同業のホテル様でも最初はそうおっしゃっていた方が、補助金で実質48万円と聞いて話だけ聞いてみると言っていただけました。資料だけでもいかがですか？」' },
  'nointerest_nouse':   { label: '必要ない', response: '「承知しました。今後インバウンドが増えた時や繁忙期前に検討される際のために、資料だけお手元に置いていただけますか？」' },
  // 他社系
  'other_using':     { label: '他社製品使用中', response: '「ありがとうございます。弊社は自社開発でオーダーメイドカスタマイズができます。IT補助金の申請代行も行っていますので、比較資料としてお送りしてもよいですか？」' },
  'other_consider':  { label: '他社で検討中', response: '「そうですか。弊社はシリンダー錠対応・13か国語・使わない月は月額0円という点で差別化しています。比較の参考に資料だけ送らせてください。」' },
  // 価格系
  'price_expensive': { label: '高そう', response: '「IT補助金を活用いただくと、KIOSK型が実質48万円〜、タブレット型が13万円〜でご導入できます。補助金申請は弊社が全部代行しますので御社のご負担はほぼゼロです。」' },
  'price_budget':    { label: '予算がない', response: '「IT補助金で最大2/3が国から補助されます。弊社が申請を全部代行しますので、タブレット型なら実質13万円〜です。資料だけでもご覧になりませんか？」' },
  // タイミング系
  'timing_later':    { label: '来年以降で', response: '「IT補助金の申請枠は毎年更新されます。今から情報を持っておくと来年すぐ動けます。今日中に資料をお送りしますのでメールアドレスをいただけますか？」' },
  'timing_busy':     { label: '繁忙期中', response: '「繁忙期前に入れた方が効果が大きいのですが、今は難しいですよね。繁忙期が落ち着いた頃に改めてご連絡してもよいですか？」' },
  // 資料系
  'info_send':       { label: '資料を送って', response: '「ありがとうございます。補助金の概要・製品仕様・導入事例をセットでお送りします。メールアドレスをいただけますか？」' },
}

const CATEGORIES = [
  { id: 'cat_busy',       label: '⏰ 忙しい',      subs: ['busy_later', 'busy_now'] },
  { id: 'cat_nointerest', label: '🚫 興味なし',    subs: ['nointerest_already', 'nointerest_nouse'] },
  { id: 'cat_other',      label: '🔀 他社使用中',  subs: ['other_using', 'other_consider'] },
  { id: 'cat_price',      label: '💰 費用・価格',  subs: ['price_expensive', 'price_budget'] },
  { id: 'cat_timing',     label: '📅 タイミング',  subs: ['timing_later', 'timing_busy'] },
  { id: 'cat_info',       label: '📋 資料希望',    subs: ['info_send'] },
]

function suggestByKeyword(kw: string): string[] {
  if (!kw.trim()) return []
  const k = kw.toLowerCase()
  return Object.entries(OBJECTION_TREE)
    .filter(([id, v]) => !id.startsWith('cat_') && (v.label.includes(kw) || v.response.includes(kw) || id.includes(k)))
    .sort((a, b) => b[1].response.length - a[1].response.length)
    .slice(0, 6)
    .map(([id]) => id)
}

type AiSuggestion = { label: string; talk: string; point: string }

const TABS = [
  { id: 'hubspot',   label: '📊 HubSpot手順',    icon: '📊' },
  { id: 'script',    label: '📞 トークスクリプト', icon: '📞' },
  { id: 'yoneyama',  label: '💰 米山パターン',    icon: '💰' },
  { id: 'status',    label: '🏷️ ステータス一覧',  icon: '🏷️' },
  { id: 'knowledge', label: '💡 商品知識',         icon: '💡' },
  { id: 'checklist', label: '✅ チェックリスト',   icon: '✅' },
  { id: 'mail',      label: '✉️ メールテンプレ',   icon: '✉️' },
]

export default function TeleapoPage() {
  const [activeTab, setActiveTab] = useState('hubspot')
  const [copiedKey, setCopiedKey] = useState<string | null>(null)
  const [selectedCat, setSelectedCat] = useState<string | null>(null)
  const [selectedResponse, setSelectedResponse] = useState<string | null>(null)
  const [searchInput, setSearchInput] = useState('')
  const suggestions = suggestByKeyword(searchInput)

  // AI切り返し
  const [aiInput, setAiInput] = useState('')
  const [aiLoading, setAiLoading] = useState(false)
  const [aiSuggestions, setAiSuggestions] = useState<AiSuggestion[]>([])
  const [aiError, setAiError] = useState<string | null>(null)
  const [aiSelectedIdx, setAiSelectedIdx] = useState<number | null>(null)
  const [aiPattern, setAiPattern] = useState<string>('yoneyama')

  const fetchAiSuggestions = useCallback(async (text: string, pattern: string) => {
    if (!text.trim()) return
    setAiLoading(true)
    setAiError(null)
    setAiSuggestions([])
    setAiSelectedIdx(null)
    try {
      const res = await fetch('/api/ai/teleapo-suggest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: text, pattern }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error ?? 'API error')
      setAiSuggestions(data.suggestions ?? [])
    } catch (e) {
      setAiError(e instanceof Error ? e.message : 'エラーが発生しました')
    } finally {
      setAiLoading(false)
    }
  }, [])

  // 米山パターン専用AI
  const [yoneyamaInput, setYoneyamaInput] = useState('')
  const [yoneyamaLoading, setYoneyamaLoading] = useState(false)
  const [yoneyamaSuggestions, setYoneyamaSuggestions] = useState<AiSuggestion[]>([])
  const [yoneyamaError, setYoneyamaError] = useState<string | null>(null)
  const [yoneyamaSelectedIdx, setYoneyamaSelectedIdx] = useState<number | null>(null)

  const fetchYoneyamaSuggestions = useCallback(async (text: string) => {
    if (!text.trim()) return
    setYoneyamaLoading(true)
    setYoneyamaError(null)
    setYoneyamaSuggestions([])
    setYoneyamaSelectedIdx(null)
    try {
      const res = await fetch('/api/ai/teleapo-suggest', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ input: text, pattern: 'yoneyama' }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error ?? 'API error')
      setYoneyamaSuggestions(data.suggestions ?? [])
    } catch (e) {
      setYoneyamaError(e instanceof Error ? e.message : 'エラーが発生しました')
    } finally {
      setYoneyamaLoading(false)
    }
  }, [])

  const copy = (text: string, key: string) => {
    navigator.clipboard.writeText(text)
    setCopiedKey(key)
    setTimeout(() => setCopiedKey(null), 2000)
  }

  const clearResponse = () => {
    setSelectedCat(null)
    setSelectedResponse(null)
  }

  const selectResponse = (id: string) => {
    setSelectedResponse(id === selectedResponse ? null : id)
  }

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">テレアポ</h1>
        <p className="text-base text-slate-400 mt-1">株式会社デバイスエージェンシー ｜ スマートチェックイン架電</p>
      </div>

      {/* 参考資料リンク */}
      <div className="mb-6 bg-slate-800 rounded-2xl border border-slate-700 p-5">
        <p className="text-base text-slate-300 font-bold mb-4">📁 参考資料</p>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
          <a href="https://app-na2.hubspot.com/contacts/39705134/objects/0-3/views/353515006/list" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-orange-900/30 hover:bg-orange-900/50 border border-orange-800/50 rounded-xl transition-colors group">
            <span className="text-2xl">🟠</span>
            <div>
              <p className="text-white text-base font-semibold group-hover:text-orange-300 transition-colors">HubSpot 架電リスト</p>
              <p className="text-slate-400 text-sm">取引一覧（楽天トラベルフィルター済）</p>
            </div>
          </a>
          <a href="https://us02web.zoom.us/myhome" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-blue-900/30 hover:bg-blue-900/50 border border-blue-800/50 rounded-xl transition-colors group">
            <span className="text-2xl">📹</span>
            <div>
              <p className="text-white text-base font-semibold group-hover:text-blue-300 transition-colors">Zoom マイホーム</p>
              <p className="text-slate-400 text-sm">架電・セミナー用 Zoom</p>
            </div>
          </a>
          <a href="https://docs.google.com/spreadsheets/d/1F2ycU3glbgrJCOkLRKHg86ROWggkbYOZXxhA2vco84o/edit?gid=767829959#gid=767829959" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-slate-700/50 hover:bg-slate-700 rounded-xl transition-colors group">
            <span className="text-2xl">📊</span>
            <div>
              <p className="text-white text-base font-semibold group-hover:text-blue-300 transition-colors">テレアポ業務マニュアル</p>
              <p className="text-slate-400 text-sm">テレアポ業務マニュアル改正シート</p>
            </div>
          </a>
          <a href="https://docs.google.com/spreadsheets/d/1WnwEhp2Db9lDHNw8qp_h2ZjhMY-mZG9TXcAAh6RX59w/edit?gid=1927965581#gid=1927965581" target="_blank" rel="noopener noreferrer"
            className="flex items-center gap-3 p-4 bg-slate-700/50 hover:bg-slate-700 rounded-xl transition-colors group">
            <span className="text-2xl">📋</span>
            <div>
              <p className="text-white text-base font-semibold group-hover:text-blue-300 transition-colors">アウトバウンド管理簿</p>
              <p className="text-slate-400 text-sm">【スマートチェックイン】架電管理</p>
            </div>
          </a>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
        {TABS.map(tab => (
          <button key={tab.id} onClick={() => setActiveTab(tab.id)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-xl text-sm font-bold whitespace-nowrap transition-all ${
              activeTab === tab.id
                ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/30'
                : 'bg-slate-800 text-slate-300 hover:bg-slate-700 border border-slate-700'
            }`}>
            {tab.label}
          </button>
        ))}
      </div>

      {/* ─── TAB: HubSpot手順 ─── */}
      {activeTab === 'hubspot' && (
        <div className="space-y-6">
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">📊 HubSpot 架電手順</h2>
            <div className="space-y-4">
              {[
                { step: '① 架電リストを開く', detail: 'HubSpot → 取引 → 「楽天トラベル（未架電）」フィルターで一覧表示', color: 'blue' },
                { step: '② 取引を選択', detail: '施設名・電話番号・過去の接触履歴を確認する', color: 'blue' },
                { step: '③ 架電', detail: 'トークスクリプトに沿って架電。担当者名を取得する', color: 'green' },
                { step: '④ 結果をステータス更新', detail: '架電後すぐにステータスを変更する（「楽天トラベル（不在）」「資料送付」等）', color: 'yellow' },
                { step: '⑤ メモを記録', detail: '担当者名・反応・次のアクションを取引メモに記録', color: 'yellow' },
                { step: '⑥ 資料送付', detail: '資料送付に至った場合は「資料送付」ステータスに変更し、メールを送る', color: 'purple' },
              ].map((item, i) => (
                <div key={i} className={`rounded-xl p-4 ${
                  item.color === 'blue' ? 'bg-blue-950/40 border border-blue-800/40' :
                  item.color === 'green' ? 'bg-green-950/40 border border-green-800/40' :
                  item.color === 'yellow' ? 'bg-yellow-950/40 border border-yellow-800/40' :
                  'bg-purple-950/40 border border-purple-800/40'
                }`}>
                  <p className={`text-sm font-bold mb-1 ${
                    item.color === 'blue' ? 'text-blue-400' :
                    item.color === 'green' ? 'text-green-400' :
                    item.color === 'yellow' ? 'text-yellow-400' : 'text-purple-400'
                  }`}>{item.step}</p>
                  <p className="text-base text-slate-200">{item.detail}</p>
                </div>
              ))}
            </div>
          </div>

          {/* HubSpotメモテンプレ */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">📝 HubSpotメモテンプレート</h2>
            <div className="space-y-3">
              {[
                { label: '不在時', text: '担当者不在。後日再架電予定。' },
                { label: '断り時', text: '「必要ない」との断り。再架電不要。ステータス：断り。' },
                { label: '資料送付時', text: '担当者：〇〇様。資料送付済み（補助金概要・製品仕様・事例）。3週間後フォロー予定。' },
                { label: 'アポ獲得時', text: 'セミナー予約済み。日時：〇月〇日〇時。Zoom URL送付済み。' },
              ].map((item, i) => (
                <div key={i} className="bg-slate-700/50 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <p className="text-sm font-bold text-slate-300">{item.label}</p>
                    <button onClick={() => copy(item.text, `hs_${i}`)}
                      className={`text-xs px-3 py-1 rounded-lg font-medium transition-colors ${copiedKey === `hs_${i}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                      {copiedKey === `hs_${i}` ? '✅' : '📋'}
                    </button>
                  </div>
                  <p className="text-base text-slate-200">{item.text}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ─── TAB: トークスクリプト ─── */}
      {activeTab === 'script' && (
        <div className="space-y-6">
          {/* AI切り返し */}
          <div className="bg-slate-900 rounded-2xl border border-purple-800/50 p-6">
            <div className="flex items-center justify-between mb-1">
              <h2 className="text-xl font-bold text-white">🤖 AI切り返しサジェスト</h2>
              <span className="text-xs bg-purple-900/60 border border-purple-700/50 text-purple-300 px-2 py-1 rounded-lg">Gemini API</span>
            </div>
            <p className="text-base text-slate-400 mb-4">相手が言ったことをそのまま入力 → AIがデバイスエージェンシーの製品切り返しを表示</p>
            <div className="flex flex-wrap gap-2 mb-4">
              {[
                { id: 'yoneyama', label: '💰 IT補助金訴求', active: 'bg-yellow-600' },
                { id: 'price',    label: '💴 価格・コスト訴求', active: 'bg-green-600' },
                { id: 'inbound',  label: '🌏 インバウンド訴求', active: 'bg-blue-600' },
                { id: 'case',     label: '🏨 導入事例訴求', active: 'bg-purple-600' },
                { id: 'urgency',  label: '⏰ 緊急性訴求', active: 'bg-red-600' },
              ].map(p => (
                <button key={p.id} onClick={() => setAiPattern(p.id)}
                  className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${aiPattern === p.id ? `${p.active} text-white` : 'bg-slate-700 text-slate-300 border border-slate-600 hover:bg-slate-600'}`}>
                  {p.label}
                </button>
              ))}
            </div>
            <div className="flex gap-2 mb-4">
              <div className="relative flex-1">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-lg">🎤</span>
                <input type="text" value={aiInput} onChange={e => setAiInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && fetchAiSuggestions(aiInput, aiPattern)}
                  placeholder="例：「もう他社のシステム入れてます」「今は忙しくて」「高そうだな」"
                  className="w-full bg-slate-800 border border-slate-600 rounded-xl pl-11 pr-4 py-4 text-base text-white placeholder-slate-500 focus:outline-none focus:border-purple-500 focus:ring-2 focus:ring-purple-500/30" />
                {aiInput && <button onClick={() => { setAiInput(''); setAiSuggestions([]); setAiSelectedIdx(null) }}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white text-xl">×</button>}
              </div>
              <button onClick={() => fetchAiSuggestions(aiInput, aiPattern)} disabled={!aiInput.trim() || aiLoading}
                className={`px-6 py-4 rounded-xl text-base font-bold transition-all whitespace-nowrap ${aiLoading ? 'bg-purple-900 text-purple-400 cursor-wait' : aiInput.trim() ? 'bg-purple-600 hover:bg-purple-500 text-white' : 'bg-slate-700 text-slate-500 cursor-not-allowed'}`}>
                {aiLoading ? '⏳ 生成中...' : '✨ AI提案'}
              </button>
            </div>
            {aiError && <div className="bg-red-950/50 border border-red-700/50 rounded-xl p-4 mb-4 text-base text-red-300">⚠️ {aiError}</div>}
            {aiLoading && <div className="text-center py-8 text-purple-400"><div className="text-2xl mb-2 animate-pulse">🤖</div><p className="text-base">Gemini AIが切り返しを生成中...</p></div>}
            {aiSuggestions.length > 0 && (
              <div>
                <p className="text-sm text-purple-400 font-bold mb-3">💡 AI推奨切り返し ({aiSuggestions.length}件)</p>
                <div className="flex flex-wrap gap-3 mb-4">
                  {aiSuggestions.map((s, i) => (
                    <button key={i} onClick={() => setAiSelectedIdx(aiSelectedIdx === i ? null : i)}
                      className={`px-5 py-3 rounded-xl text-base font-bold transition-all ${aiSelectedIdx === i ? 'bg-purple-600 text-white shadow-lg scale-105' : 'bg-purple-900/50 text-purple-200 hover:bg-purple-700 hover:text-white border border-purple-700/60'}`}>
                      {s.label}
                    </button>
                  ))}
                </div>
                {aiSelectedIdx !== null && aiSuggestions[aiSelectedIdx] && (
                  <div className="bg-purple-950/60 border-2 border-purple-700/70 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <p className="text-base text-purple-400 font-bold">💬 {aiSuggestions[aiSelectedIdx].label}</p>
                        <p className="text-sm text-purple-300/70 mt-0.5">📌 {aiSuggestions[aiSelectedIdx].point}</p>
                      </div>
                      <button onClick={() => copy(aiSuggestions[aiSelectedIdx!].talk, 'ai_talk')}
                        className={`px-5 py-2 rounded-xl text-sm font-bold transition-colors ${copiedKey === 'ai_talk' ? 'bg-purple-600 text-white' : 'bg-slate-700 hover:bg-slate-600 text-slate-200'}`}>
                        {copiedKey === 'ai_talk' ? '✅ コピー済み' : '📋 コピー'}
                      </button>
                    </div>
                    <p className="text-lg text-white leading-relaxed font-medium">{aiSuggestions[aiSelectedIdx].talk}</p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* キーワード検索 */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-3">🔍 キーワードで切り返しを検索</h2>
            <input type="text" value={searchInput} onChange={e => setSearchInput(e.target.value)}
              placeholder="例：予算・他社・忙しい・インバウンド"
              className="w-full bg-slate-700 border border-slate-600 rounded-xl px-4 py-3 text-base text-white placeholder-slate-500 focus:outline-none focus:border-blue-500" />
            {suggestions.length > 0 && (
              <div className="mt-3 space-y-2">
                {suggestions.map(id => (
                  <div key={id} className="bg-slate-700/60 rounded-xl p-4">
                    <p className="text-sm font-bold text-slate-300 mb-1">{OBJECTION_TREE[id].label}</p>
                    <div className="flex items-start gap-3">
                      <p className="text-base text-slate-200 flex-1">{OBJECTION_TREE[id].response}</p>
                      <button onClick={() => copy(OBJECTION_TREE[id].response, `search_${id}`)}
                        className={`text-xs px-3 py-1 rounded-lg flex-shrink-0 transition-colors ${copiedKey === `search_${id}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                        {copiedKey === `search_${id}` ? '✅' : '📋'}
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* 切り返しツリー */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-base font-bold text-white">🔄 断り文句別 切り返しツリー</h2>
              {selectedCat && <button onClick={clearResponse} className="text-xs text-slate-400 hover:text-white">← 戻る</button>}
            </div>
            {!selectedCat ? (
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {CATEGORIES.map(cat => (
                  <button key={cat.id} onClick={() => setSelectedCat(cat.id)}
                    className="bg-slate-700/60 hover:bg-slate-700 border border-slate-600 rounded-xl p-4 text-left transition-colors">
                    <p className="text-base font-bold text-white">{cat.label}</p>
                    <p className="text-xs text-slate-400 mt-1">{cat.subs.length}パターン</p>
                  </button>
                ))}
              </div>
            ) : (
              <div className="space-y-3">
                <div className="flex flex-wrap gap-2 mb-4">
                  {CATEGORIES.find(c => c.id === selectedCat)?.subs.map(subId => (
                    <button key={subId} onClick={() => selectResponse(subId)}
                      className={`px-4 py-2 rounded-xl text-sm font-bold transition-all ${selectedResponse === subId ? 'bg-blue-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600 border border-slate-600'}`}>
                      {OBJECTION_TREE[subId]?.label}
                    </button>
                  ))}
                </div>
                {selectedResponse && OBJECTION_TREE[selectedResponse] && (
                  <div className="bg-blue-950/40 border border-blue-800/50 rounded-xl p-5">
                    <div className="flex items-center justify-between mb-3">
                      <p className="text-base font-bold text-blue-300">{OBJECTION_TREE[selectedResponse].label}</p>
                      <button onClick={() => copy(OBJECTION_TREE[selectedResponse].response, 'tree_resp')}
                        className={`text-sm px-4 py-2 rounded-xl font-bold transition-colors ${copiedKey === 'tree_resp' ? 'bg-green-600 text-white' : 'bg-slate-700 hover:bg-slate-600 text-slate-200'}`}>
                        {copiedKey === 'tree_resp' ? '✅ コピー済み' : '📋 コピー'}
                      </button>
                    </div>
                    <p className="text-base text-white leading-relaxed">{OBJECTION_TREE[selectedResponse].response}</p>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* ─── TAB: 米山パターン ─── */}
      {activeTab === 'yoneyama' && (
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-yellow-900/40 to-orange-900/40 border border-yellow-700/50 rounded-2xl p-6">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-3xl">💰</span>
              <div>
                <h2 className="text-xl font-bold text-white">米山パターン — IT補助金全面訴求型</h2>
                <p className="text-base text-yellow-300/80 mt-0.5">政府の積極支援・補助金申請代行を前面に出し、コスト障壁を最初に取り除くアプローチ</p>
              </div>
            </div>
          </div>

          {/* 米山パターン専用AI */}
          <div className="bg-slate-900 rounded-2xl border border-yellow-800/50 p-6">
            <div className="flex items-center justify-between mb-1">
              <h2 className="text-xl font-bold text-white">🤖 AI切り返し（米山パターン専用）</h2>
              <span className="text-xs bg-yellow-900/60 border border-yellow-700/50 text-yellow-300 px-2 py-1 rounded-lg">Gemini API</span>
            </div>
            <p className="text-base text-slate-400 mb-4">相手の発言を入力 → IT補助金訴求を含む切り返しをAIが生成</p>
            <div className="flex gap-2 mb-4">
              <div className="relative flex-1">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 text-lg">🎤</span>
                <input type="text" value={yoneyamaInput} onChange={e => setYoneyamaInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && fetchYoneyamaSuggestions(yoneyamaInput)}
                  placeholder="例：「予算がない」「他社で検討中」「今は時期が悪い」"
                  className="w-full bg-slate-800 border border-slate-600 rounded-xl pl-11 pr-4 py-4 text-base text-white placeholder-slate-500 focus:outline-none focus:border-yellow-500 focus:ring-2 focus:ring-yellow-500/30" />
                {yoneyamaInput && <button onClick={() => { setYoneyamaInput(''); setYoneyamaSuggestions([]); setYoneyamaSelectedIdx(null) }}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white text-xl">×</button>}
              </div>
              <button onClick={() => fetchYoneyamaSuggestions(yoneyamaInput)} disabled={!yoneyamaInput.trim() || yoneyamaLoading}
                className={`px-6 py-4 rounded-xl text-base font-bold transition-all whitespace-nowrap ${yoneyamaLoading ? 'bg-yellow-900 text-yellow-400 cursor-wait' : yoneyamaInput.trim() ? 'bg-yellow-600 hover:bg-yellow-500 text-white' : 'bg-slate-700 text-slate-500 cursor-not-allowed'}`}>
                {yoneyamaLoading ? '⏳ 生成中...' : '✨ AI提案'}
              </button>
            </div>
            {yoneyamaError && <div className="bg-red-950/50 border border-red-700/50 rounded-xl p-4 mb-4 text-base text-red-300">⚠️ {yoneyamaError}</div>}
            {yoneyamaLoading && <div className="text-center py-8 text-yellow-400"><div className="text-2xl mb-2 animate-pulse">🤖</div><p className="text-base">Gemini AIが米山パターンで生成中...</p></div>}
            {yoneyamaSuggestions.length > 0 && (
              <div>
                <p className="text-sm text-yellow-400 font-bold mb-3">💡 AI推奨切り返し ({yoneyamaSuggestions.length}件)</p>
                <div className="flex flex-wrap gap-3 mb-4">
                  {yoneyamaSuggestions.map((s, i) => (
                    <button key={i} onClick={() => setYoneyamaSelectedIdx(yoneyamaSelectedIdx === i ? null : i)}
                      className={`px-5 py-3 rounded-xl text-base font-bold transition-all ${yoneyamaSelectedIdx === i ? 'bg-yellow-600 text-white shadow-lg scale-105' : 'bg-yellow-900/50 text-yellow-200 hover:bg-yellow-700 hover:text-white border border-yellow-700/60'}`}>
                      {s.label}
                    </button>
                  ))}
                </div>
                {yoneyamaSelectedIdx !== null && yoneyamaSuggestions[yoneyamaSelectedIdx] && (
                  <div className="bg-yellow-950/60 border-2 border-yellow-700/70 rounded-2xl p-6">
                    <div className="flex items-center justify-between mb-3">
                      <div>
                        <p className="text-base text-yellow-400 font-bold">💬 {yoneyamaSuggestions[yoneyamaSelectedIdx].label}</p>
                        <p className="text-sm text-yellow-300/70 mt-0.5">📌 {yoneyamaSuggestions[yoneyamaSelectedIdx].point}</p>
                      </div>
                      <button onClick={() => copy(yoneyamaSuggestions[yoneyamaSelectedIdx!].talk, 'yoneyama_ai')}
                        className={`px-5 py-2 rounded-xl text-sm font-bold transition-colors ${copiedKey === 'yoneyama_ai' ? 'bg-yellow-600 text-white' : 'bg-slate-700 hover:bg-slate-600 text-slate-200'}`}>
                        {copiedKey === 'yoneyama_ai' ? '✅ コピー済み' : '📋 コピー'}
                      </button>
                    </div>
                    <p className="text-lg text-white leading-relaxed font-medium">{yoneyamaSuggestions[yoneyamaSelectedIdx].talk}</p>
                  </div>
                )}
              </div>
            )}
          </div>

          {/* 米山パターン スクリプト */}
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">📞 米山パターン — トークスクリプト</h2>
            <div className="space-y-4">
              {[
                {
                  label: 'STEP 1｜受付突破 — 担当者につなぐ',
                  color: 'blue',
                  text: '「お電話失礼いたします。デバイスエージェンシーの米山でございます。\nホテル・旅館様向けのIT補助金のご案内でご連絡しているのですが、\nご支配人様か、ご担当者様はいらっしゃいますでしょうか？」',
                  point: 'IT補助金のご案内と言うだけで受付に止められにくくなる。「支配人様か担当者様」と二択にすることで名前がなくても取り次ぎを引き出せる。',
                },
                {
                  label: 'STEP 2｜担当者への第一声 — 自然な補助金訴求',
                  color: 'yellow',
                  text: '「ありがとうございます。実はいま国のIT補助金を使って、\n自動チェックイン機をKIOSK型なら実質48万円〜、タブレット型なら13万円〜でご導入できる制度がありまして、\n補助金の申請も弊社が全部代行しています。今日は売り込みではなく、その制度のご案内でご連絡しました。\n今、2〜3分だけよろしいでしょうか？」',
                  point: '「売り込みではなく」を明言するだけで警戒心が大きく下がる。金額を先に言うことで「高いんでしょ」という先入観を防ぐ。',
                },
                {
                  label: 'STEP 3｜ヒアリング — 課題を自然に引き出す',
                  color: 'purple',
                  text: '「最近、うちの周りのホテル様からも夜間の対応とかインバウンドのお客様への対応で\n大変という声をよく聞くんですが、御社では今、何か運用で課題に感じているところはありますか？」',
                  point: '具体例（夜間対応・インバウンド等）を出すことで課題を引き出しやすくなる。課題が出たら→IT補助金で解決された事例があります、につなぐ。',
                },
                {
                  label: 'STEP 4｜課題あり → 事例提案 → アポ取り',
                  color: 'green',
                  text: '「そうですよね。実は、その課題をIT補助金を使ってうまく解決されているホテル様の事例が手元にあります。\n資料と補助金の申請スケジュールをメールでお送りしてもいいですか？\nその後、15分だけいただいて、補助金を使った具体的なご説明ができればと思いまして。」',
                  point: '「資料を送る」→「15分だけ」の2段階でアポのハードルを下げる。日程は来週の火曜か水曜どちらが？と二択で聞く。',
                },
                {
                  label: "STEP 4'｜課題なし → 情報だけ置いて次につなぐ",
                  color: 'slate',
                  text: '「そうですか。IT補助金って毎年申請枠があるので、タイミングが来たときのために情報だけ持っておいてもらえれば十分です。\n補助金の概要と製品の資料をメールでお送りしてもいいですか？\nメールアドレスをいただければ今日中に送ります。」',
                  point: '「資料送付 → 3週間以内に再架電」でインセンティブ対象を狙う。メアドが取れたら施設名・担当者名をHubSpotに記録する。',
                },
              ].map((item, i) => (
                <div key={i} className={`rounded-xl p-5 ${
                  item.color === 'blue' ? 'bg-blue-950/40 border border-blue-800/40' :
                  item.color === 'yellow' ? 'bg-yellow-950/40 border border-yellow-800/40' :
                  item.color === 'purple' ? 'bg-purple-950/40 border border-purple-800/40' :
                  item.color === 'green' ? 'bg-green-950/40 border border-green-800/40' :
                  'bg-slate-700/50 border border-slate-600/40'
                }`}>
                  <div className="flex items-center justify-between mb-3">
                    <p className={`text-base font-bold ${
                      item.color === 'blue' ? 'text-blue-400' :
                      item.color === 'yellow' ? 'text-yellow-400' :
                      item.color === 'purple' ? 'text-purple-400' :
                      item.color === 'green' ? 'text-green-400' : 'text-slate-400'
                    }`}>{item.label}</p>
                    <button onClick={() => copy(item.text, `ym_${i}`)}
                      className={`text-sm px-3 py-1.5 rounded-lg font-medium transition-colors ${copiedKey === `ym_${i}` ? 'bg-green-600 text-white' : 'bg-slate-700 text-slate-300 hover:bg-slate-600'}`}>
                      {copiedKey === `ym_${i}` ? '✅' : '📋'}
                    </button>
                  </div>
                  <p className="text-base text-slate-100 leading-relaxed whitespace-pre-line mb-3">{item.text}</p>
                  <p className="text-sm text-slate-400 leading-relaxed border-t border-slate-600/50 pt-3">💡 {item.point}</p>
                </div>
              ))}
            </div>
          </div>

          {/* 断り文句別切り返し（IT補助金訴求） */}
          <div className="bg-slate-800 rounded-2xl border border-yellow-700/40 p-6">
            <h2 className="text-xl font-bold text-white mb-4">🔄 断り文句別 切り返し（IT補助金訴求）</h2>
            <div className="space-y-3">
              {[
                { obj: '「予算がない」「お金がかかる」', res: '「そうですよね。実はIT補助金を活用していただくと、弊社が申請を全て代行しますので、KIOSK型が48万円〜、タブレット型が13万円〜でご導入できます。月額費用も使わない月は0円なので、繁忙期だけのご利用も可能です。資料だけでもご覧になりませんか？」' },
                { obj: '「他社製品を検討・使用中」', res: '「弊社はシリンダー錠対応・完全オーダーメイドカスタマイズという点で差別化できています。またIT補助金の申請代行は弊社の強みです。比較検討の資料としてお送りしてもよろしいでしょうか？」' },
                { obj: '「今は時期が悪い」「来年以降で」', res: '「IT補助金の申請枠は毎年更新されますので、今すぐでなくても情報だけ持っておいていただくと、タイミングが来た時にすぐ動けます。今日中に資料をメールでお送りするだけですので、メールアドレスをお教えいただけますか？」' },
                { obj: '「補助金って何ですか？」', res: '「IT導入補助金というもので、中小企業様がITシステムを導入する際に国が費用の最大2/3を補助してくれる制度です。弊社は申請手続きを全て代行しておりますので、御社は書類を揃えていただくだけでOKです。」' },
              ].map((item, i) => (
                <div key={i} className="bg-slate-700/50 rounded-xl p-4">
                  <p className="text-base font-bold text-red-400 mb-2">❌ {item.obj}</p>
                  <div className="flex items-start gap-3">
                    <p className="text-base text-slate-200 leading-relaxed flex-1">✅ {item.res}</p>
                    <button onClick={() => copy(item.res, `ym_obj_${i}`)}
                      className={`text-xs px-3 py-1 rounded-lg font-medium flex-shrink-0 transition-colors ${copiedKey === `ym_obj_${i}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                      {copiedKey === `ym_obj_${i}` ? '✅' : '📋'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ─── TAB: ステータス一覧 ─── */}
      {activeTab === 'status' && (
        <div className="space-y-6">
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">✅ 使用するステータス（取引ステージ）</h2>
            <div className="overflow-x-auto">
              <table className="w-full text-base">
                <thead>
                  <tr className="border-b border-slate-700">
                    <th className="text-left text-slate-400 font-medium py-2 pr-4">ステータス</th>
                    <th className="text-left text-slate-400 font-medium py-2">用途</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-700/50">
                  {[
                    { status: '楽天トラベル（未架電）', desc: 'ターゲットリスト', badge: 'blue' },
                    { status: '楽天トラベル（不在）', desc: '担当者不在時（資料送付後の不在は移動不要）', badge: 'yellow' },
                    { status: '楽天トラベル（断り）', desc: '断られた場合', badge: 'red' },
                    { status: '楽天トラベル（本社へ）', desc: '本社が決済の場合', badge: 'purple' },
                    { status: '楽天トラベル（1回目）', desc: '1回目のアプローチ', badge: 'slate' },
                    { status: '資料送付', desc: '架電後に資料送付に至った場合', badge: 'green' },
                    { status: '架電クレーム', desc: '「かけてくるな」など言われた場合', badge: 'red' },
                    { status: '架電リスト（他社製品使用）', desc: 'すでに他社製品を導入済みの場合', badge: 'slate' },
                    { status: '連絡不可・IVR', desc: '閉業や電話番号が使われていない場合', badge: 'slate' },
                    { status: 'セミナー予定', desc: 'アポイント獲得〜当日まで', badge: 'green' },
                    { status: 'セミナー参加', desc: '実際に参加した場合', badge: 'green' },
                    { status: 'セミナーキャンセル', desc: 'キャンセルが発生した場合', badge: 'red' },
                  ].map((row, i) => (
                    <tr key={i}>
                      <td className="py-3 pr-4">
                        <span className={`text-sm font-medium px-2 py-1 rounded-lg ${
                          row.badge === 'blue' ? 'bg-blue-900/60 text-blue-300' :
                          row.badge === 'green' ? 'bg-green-900/60 text-green-300' :
                          row.badge === 'yellow' ? 'bg-yellow-900/60 text-yellow-300' :
                          row.badge === 'red' ? 'bg-red-900/60 text-red-300' :
                          row.badge === 'purple' ? 'bg-purple-900/60 text-purple-300' :
                          'bg-slate-700 text-slate-300'
                        }`}>{row.status}</span>
                      </td>
                      <td className="text-slate-300 py-3 text-base">{row.desc}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ─── TAB: 商品知識 ─── */}
      {activeTab === 'knowledge' && (
        <div className="space-y-6">
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">💡 製品ラインナップ</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {[
                { name: 'KIOSK型 自動チェックイン機', price: '実質48万円〜（IT補助金適用後）', features: ['13か国語対応', 'パスポートスキャン', 'クレジット・交通系IC決済', '領収書発行', 'PMS連携'] },
                { name: 'タブレット型 自動チェックイン機', price: '実質13万円〜（IT補助金適用後）', features: ['省スペース', 'フロント補助として活用', 'シリンダー錠対応', '小規模旅館向け'] },
                { name: 'クラウドスマートロック', price: '別途見積もり', features: ['暗証番号で開錠', 'スマホアプリ対応', 'シリンダー錠も可', '遠隔管理'] },
                { name: 'ルームタブレット', price: '別途見積もり', features: ['客室内電話代替', 'アメニティ注文', 'チェックアウト対応', '多言語対応'] },
              ].map((p, i) => (
                <div key={i} className="bg-slate-700/50 rounded-xl p-5 border border-slate-600">
                  <p className="text-base font-bold text-white mb-1">{p.name}</p>
                  <p className="text-yellow-400 text-sm font-bold mb-3">{p.price}</p>
                  <ul className="space-y-1">
                    {p.features.map((f, j) => (
                      <li key={j} className="text-base text-slate-300 flex items-center gap-2">
                        <span className="text-green-400 text-xs">✓</span> {f}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">🔑 訴求ポイント（必ず覚える）</h2>
            <div className="space-y-3">
              {[
                { icon: '💰', title: 'IT補助金申請代行', desc: '中小企業デジタル化補助金・IT導入補助金を活用。最大2/3補助。申請手続きは弊社が全て代行。' },
                { icon: '🌏', title: '13か国語対応', desc: 'インバウンド対策に最適。パスポートスキャン機能で外国人チェックインもスムーズ。' },
                { icon: '🔧', title: '完全オーダーメイド', desc: '自社開発のためカスタマイズ自由。PMS連携実績：ステイシー・スイートブック・ベッド4。' },
                { icon: '📅', title: '月額0円プラン', desc: '使わない期間は月額0円。季節限定利用OK。閑散期のコスト負担なし。' },
                { icon: '📹', title: '無料セミナー', desc: '毎週水曜11時・金曜13時。Zoomで無料参加可。全国対応。' },
              ].map((item, i) => (
                <div key={i} className="flex items-start gap-4 p-4 bg-slate-700/40 rounded-xl">
                  <span className="text-2xl flex-shrink-0">{item.icon}</span>
                  <div>
                    <p className="text-base font-bold text-white">{item.title}</p>
                    <p className="text-base text-slate-300 mt-1">{item.desc}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ─── TAB: チェックリスト ─── */}
      {activeTab === 'checklist' && (
        <div className="space-y-6">
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">✅ 架電前チェックリスト</h2>
            <div className="space-y-2">
              {[
                '施設名・電話番号・過去の接触履歴をHubSpotで確認した',
                'トークスクリプトを一度声に出して確認した',
                'VOICEVOXやZoomなど架電ツールが起動している',
                'メモ帳（HubSpot）を開いている',
                '資料送付用のメールテンプレートを準備している',
                'セミナー日程（今週分）を把握している',
              ].map((item, i) => (
                <label key={i} className="flex items-center gap-3 p-3 rounded-xl hover:bg-slate-700/40 cursor-pointer">
                  <input type="checkbox" className="w-5 h-5 rounded accent-blue-500" />
                  <span className="text-base text-slate-200">{item}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-base font-bold text-white mb-4">✅ 架電後チェックリスト</h2>
            <div className="space-y-2">
              {[
                'HubSpotのステータスを更新した',
                '担当者名・反応・次のアクションをメモした',
                '資料送付の場合：メールを今日中に送った',
                'アポ獲得の場合：セミナーURLをメールで送った',
                '断りの場合：「楽天トラベル（断り）」に変更した',
              ].map((item, i) => (
                <label key={i} className="flex items-center gap-3 p-3 rounded-xl hover:bg-slate-700/40 cursor-pointer">
                  <input type="checkbox" className="w-5 h-5 rounded accent-blue-500" />
                  <span className="text-base text-slate-200">{item}</span>
                </label>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ─── TAB: メールテンプレ ─── */}
      {activeTab === 'mail' && (
        <div className="space-y-6">
          <div className="bg-slate-800 rounded-2xl border border-slate-700 p-6">
            <h2 className="text-xl font-bold text-white mb-4">✉️ メールテンプレート</h2>
            <div className="space-y-4">
              {[
                {
                  label: '資料送付メール',
                  subject: '【IT補助金活用】自動チェックイン機のご案内 / デバイスエージェンシー',
                  body: `〇〇様

先ほどはお電話ありがとうございました。
デバイスエージェンシーの米山でございます。

ご案内いたしました自動チェックイン機の資料をお送りします。

【製品概要】
・KIOSK型：IT補助金適用後 実質48万円〜
・タブレット型：IT補助金適用後 実質13万円〜
・補助金申請は弊社が全て代行
・13か国語対応・使わない月は月額0円

【無料セミナーのご案内】
毎週水曜11時・金曜13時（Zoom・無料）
ご都合のよい日時をお教えください。

ご不明点がありましたらお気軽にご連絡ください。

─────────────────────────
株式会社デバイスエージェンシー
米山 文貴
TEL: 080-3207-8422
─────────────────────────`,
                },
                {
                  label: 'セミナー案内メール',
                  subject: '【無料セミナーご案内】自動チェックイン機 × IT補助金 / デバイスエージェンシー',
                  body: `〇〇様

この度はセミナーへのご参加ありがとうございます。
デバイスエージェンシーの米山でございます。

以下の日時でZoomセミナーを開催いたします。

【セミナー詳細】
日時：〇月〇日（〇）〇〇:〇〇〜
形式：Zoom（オンライン・無料）
内容：IT補助金活用方法 / 製品デモ / Q&A

ZoomミーティングURL：
https://us02web.zoom.us/j/XXXXXXXXXX

ご参加をお待ちしております。

─────────────────────────
株式会社デバイスエージェンシー
米山 文貴
─────────────────────────`,
                },
              ].map((tmpl, i) => (
                <div key={i} className="bg-slate-700/50 rounded-xl p-5">
                  <div className="flex items-center justify-between mb-3">
                    <p className="text-base font-bold text-white">{tmpl.label}</p>
                    <div className="flex gap-2">
                      <button onClick={() => copy(tmpl.subject, `subj_${i}`)}
                        className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${copiedKey === `subj_${i}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                        {copiedKey === `subj_${i}` ? '✅件名' : '📋 件名'}
                      </button>
                      <button onClick={() => copy(tmpl.body, `body_${i}`)}
                        className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors ${copiedKey === `body_${i}` ? 'bg-green-600 text-white' : 'bg-slate-600 text-slate-300 hover:bg-slate-500'}`}>
                        {copiedKey === `body_${i}` ? '✅本文' : '📋 本文'}
                      </button>
                    </div>
                  </div>
                  <p className="text-sm text-slate-400 mb-1">件名：</p>
                  <p className="text-base text-blue-300 mb-3">{tmpl.subject}</p>
                  <pre className="text-base text-slate-200 leading-relaxed whitespace-pre-wrap font-sans">{tmpl.body}</pre>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

    </div>
  )
}
