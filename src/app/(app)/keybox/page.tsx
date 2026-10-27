'use client'

import { useState, useEffect } from 'react'

// 進行中案件タスク（初期データ：カーステーション星光）
type CaseTask = { id: number; task: string; who: string; via: string; done: boolean; memo: string }
type ActiveCase = { name: string; tasks: CaseTask[] }
const TASKS_STORAGE_KEY = 'keybox_active_cases_v1'
const DEFAULT_CASES: ActiveCase[] = [
  {
    name: 'カーステーション星光（THE ART MEIBOKU・別府市）KBL16×1台 納品希望12/24',
    tasks: [
      { id: 1, task: '寸法確認（転倒防止込みD600mmで正か）＋発注金額確認', who: '今津さん', via: 'Slack', done: false, memo: '単体発注赤字見込み→同時発注可否も確認' },
      { id: 2, task: '状況報告（図面了承済・置台は先方製作・請求金額10万円確認済）', who: '橋本さん', via: 'Slack', done: false, memo: '請求金額は申込書で判明済み' },
      { id: 3, task: '粗利計算（請求10万円−発注金額）', who: '自分', via: 'このページ', done: false, memo: '試算: 発注約136,267円→▲36,267円赤字' },
      { id: 4, task: '社長承認メール送信', who: '田中社長', via: 'メール', done: false, memo: '請求/発注/粗利3点セット必須。赤字なら理由と対策明記' },
      { id: 5, task: '正式発注依頼', who: '今津さん', via: 'Slack', done: false, memo: '社長承認後。一斉発注から外れ後追い' },
      { id: 6, task: '手配完了連絡', who: '池島様（星光）', via: 'メール', done: false, memo: '発注後に連絡でOK' },
      { id: 7, task: '発注フローをNotionマニュアル化', who: '自分', via: 'Notion', done: false, memo: '社長指摘: 3点セット必須ルールを記録' },
    ],
  },
]

// キーボックス単価テーブル（USD）※32BOX実績670USD基準で補間）
const PRICE_TABLE = [
  { size: 15, usd: 600, note: '旧料金: 20万円' },
  { size: 16, usd: 610, note: '旧料金なし → 15P代用' },
  { size: 20, usd: 550, note: '実績値' },
  { size: 28, usd: 670, note: '32BOX単価を代用（旧料金なし → 30P代用）' },
  { size: 30, usd: 670, note: '旧料金: 25万円（新料金: 28P→26万）' },
  { size: 32, usd: 670, note: '実績値（ルミエール日向）' },
  { size: 42, usd: 800, note: '実績値' },
]

// 重量参考（kg）
const WEIGHT_MAP: Record<number, number> = {
  15: 50, 16: 50, 20: 60, 28: 80, 30: 80, 32: 80, 42: 100,
}

// 中国輸送費単価（円/kg）— ルミエール日向実績: 33,700÷130kg
const CHINA_FREIGHT_PER_KG = 259.23

// JITBOX概算（円）
const JITBOX_PRESETS = [
  { label: '大阪 → 栃木日光', cost: 30000 },
  { label: '大阪 → 長野塩尻', cost: 21000 },
  { label: '大阪 → 北海道倶知安', cost: 71000 },
  { label: '大阪 → 北海道道央(なんぽろ)', cost: 70285 },
  { label: '大阪 → 内地(混載便)', cost: 27535 },
  { label: 'カスタム', cost: 0 },
]

// 発注フロー
const FLOW_STEPS = [
  { step: 1, title: '申込書・見積書の受領', detail: '先方から申込書・見積書を受け取り、請求書先アドレスとアカウントアドレスを確認する。' },
  { step: 2, title: 'PMS連携確認', detail: 'PMS新規連携が必要な場合はHOD（堀内）に早めに相談。開発期間が読めない場合は先行着手を依頼。' },
  { step: 3, title: 'キーボックスサイズ確認', detail: '部屋数からBOX数を確定。設置スペース（サーキュレーター等の障害物）・寸法を先方に確認。KIOSKと並べる場合は2m以内に収まるかチェック。\n例：23部屋 → 28BOX（7×4）推奨' },
  { step: 4, title: '入金確認', detail: '補助金採択後の案件は入金タイミングを確認。入金確認後に機器手配を開始するのが原則。例外（同時発注）は社長承認が必要。' },
  { step: 5, title: '粗利計算・社長承認依頼', detail: '以下を揃えて社長へ承認メールを送付：\n・発注金額（本体USD×レート＋中国輸送費＋JITBOX）\n・請求金額\n・粗利益\n※旧料金適用の例外がある場合は必ず明記。件名：※田中社長確認 キーボックス発注依頼[日付]' },
  { step: 6, title: 'キーボックス発注', detail: '社長承認メール返信後、今津（STG）へ発注依頼。複数案件は同時発注で輸送費を圧縮できるか検討。単体発注は原価が上がるため注意。' },
  { step: 7, title: '納品・設置', detail: '12月納品希望の場合は逆算してキーボックスを先行手配（調達に約3ヶ月）。KIOSKとキーボックスの設置位置・接続を確認。' },
]

// 承認メールテンプレート生成
function genApprovalMail(items: { company: string; property: string; size: number; cost: number; revenue: number; profit: number; paid: boolean; exception: boolean }[]) {
  const today = new Date().toISOString().slice(0, 10).replace(/-/g, '')
  const lines = items.map((it, i) => {
    const sym = it.profit < 0 ? '▲' : ''
    return `\
${['①', '②', '③', '④', '⑤'][i]} 担当：[担当者名]
　企業名：${it.company}
　物件名：${it.property}
　${it.size}BOX：1台
　発注金額：${it.cost.toLocaleString()}円　請求金額：${it.revenue.toLocaleString()}円　粗利：${sym}${Math.abs(it.profit).toLocaleString()}円${it.exception ? '（価格改定前旧料金適用・例外）' : ''}
　入金：${it.paid ? '済み' : '未入金（同時発注申請）'}`
  }).join('\n\n')
  return `件名：※田中社長確認 キーボックス発注依頼${today}

お疲れ様です。

下記${items.length}件、キーボックス納品の為、手配依頼となります。

${lines}

ご確認・ご承認のほどよろしくお願いいたします。

以上、よろしくお願いいたします。`
}

export default function KeyboxPage() {
  const [rate, setRate] = useState(157)
  const [size, setSize] = useState(28)
  const [customUsd, setCustomUsd] = useState('')
  const [customWeight, setCustomWeight] = useState('')
  const [jitboxPreset, setJitboxPreset] = useState(0)
  const [jitboxCustom, setJitboxCustom] = useState('')
  const [revenue, setRevenue] = useState(150000)

  const [items, setItems] = useState<{ company: string; property: string; size: number; cost: number; revenue: number; profit: number; paid: boolean; exception: boolean }[]>([])
  const [company, setCompany] = useState('')
  const [property, setProperty] = useState('')
  const [paid, setPaid] = useState(true)
  const [exception, setException] = useState(false)
  const [mailText, setMailText] = useState('')
  const [mailCopied, setMailCopied] = useState(false)

  // 進行中案件タスク（localStorage永続化）
  const [cases, setCases] = useState<ActiveCase[]>(DEFAULT_CASES)
  const [casesLoaded, setCasesLoaded] = useState(false)
  useEffect(() => {
    try {
      const raw = localStorage.getItem(TASKS_STORAGE_KEY)
      if (raw) setCases(JSON.parse(raw))
    } catch { /* ignore */ }
    setCasesLoaded(true)
  }, [])
  useEffect(() => {
    if (casesLoaded) localStorage.setItem(TASKS_STORAGE_KEY, JSON.stringify(cases))
  }, [cases, casesLoaded])
  const toggleTask = (ci: number, tid: number) => {
    setCases(prev => prev.map((c, i) => i !== ci ? c : {
      ...c,
      tasks: c.tasks.map(t => t.id === tid ? { ...t, done: !t.done } : t),
    }))
  }
  const removeCase = (ci: number) => {
    if (!confirm('この案件のタスクリストを削除しますか？')) return
    setCases(prev => prev.filter((_, i) => i !== ci))
  }

  // 計算
  const priceRow = PRICE_TABLE.find(p => p.size === size) ?? PRICE_TABLE[PRICE_TABLE.length - 1]
  const usd = customUsd ? Number(customUsd) : priceRow.usd
  const weight = customWeight ? Number(customWeight) : (WEIGHT_MAP[size] ?? 80)
  const jitboxRow = JITBOX_PRESETS[jitboxPreset]
  const jitboxCost = jitboxPreset === JITBOX_PRESETS.length - 1 ? Number(jitboxCustom || 0) : jitboxRow.cost
  const body = Math.round(usd * rate)
  const freight = Math.round(weight * CHINA_FREIGHT_PER_KG)
  const total = body + freight + jitboxCost
  const profit = revenue - total

  const addItem = () => {
    if (!company || !property) return
    setItems(prev => [...prev, { company, property, size, cost: total, revenue, profit, paid, exception }])
    setCompany('')
    setProperty('')
  }

  const removeItem = (i: number) => setItems(prev => prev.filter((_, idx) => idx !== i))

  const genMail = () => {
    setMailText(genApprovalMail(items))
  }

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-white">📦 キーボックス 単価・発注管理</h1>
        <p className="text-slate-400 text-base mt-1">単価計算 / 粗利シミュレーション / 社長承認メール生成</p>
      </div>

      {/* 進行中案件タスク */}
      {cases.length > 0 && (
        <div className="mb-5 space-y-4">
          {cases.map((c, ci) => {
            const doneCount = c.tasks.filter(t => t.done).length
            return (
              <div key={ci} className="bg-slate-800 border border-amber-700/50 rounded-2xl p-5">
                <div className="flex items-center justify-between mb-3">
                  <p className="text-base font-semibold text-white">
                    📋 進行中案件：{c.name}
                    <span className={`ml-3 text-sm ${doneCount === c.tasks.length ? 'text-emerald-400' : 'text-amber-400'}`}>
                      {doneCount}/{c.tasks.length} 完了
                    </span>
                  </p>
                  <button onClick={() => removeCase(ci)} className="text-slate-500 hover:text-red-400 text-sm">案件を削除</button>
                </div>
                <div className="space-y-1.5">
                  {c.tasks.map(t => (
                    <label key={t.id} className={`flex items-start gap-3 bg-slate-900 rounded-lg px-3 py-2 cursor-pointer ${t.done ? 'opacity-50' : ''}`}>
                      <input type="checkbox" checked={t.done} onChange={() => toggleTask(ci, t.id)} className="accent-emerald-500 mt-1" />
                      <div className="flex-1 text-base">
                        <span className={`text-white ${t.done ? 'line-through' : ''}`}>{t.task}</span>
                        <span className="ml-2 text-blue-300">→ {t.who}</span>
                        <span className="ml-1 text-slate-500">[{t.via}]</span>
                        {t.memo && <p className="text-slate-400 text-sm mt-0.5">{t.memo}</p>}
                      </div>
                    </label>
                  ))}
                </div>
              </div>
            )
          })}
        </div>
      )}

      <div className="grid grid-cols-2 gap-5 items-start">

        {/* 左：粗利計算 */}
        <div className="flex flex-col gap-4">

          {/* 単価テーブル */}
          <div className="bg-slate-800 border border-slate-700 rounded-2xl p-5">
            <p className="text-base font-semibold text-white mb-3">📋 キーボックス参考単価（USD）</p>
            <table className="w-full text-base">
              <thead>
                <tr className="text-slate-400 border-b border-slate-700">
                  <th className="pb-2 text-left">サイズ</th>
                  <th className="pb-2 text-right">USD</th>
                  <th className="pb-2 text-right">重量(kg)</th>
                  <th className="pb-2 text-left pl-3">備考</th>
                </tr>
              </thead>
              <tbody>
                {PRICE_TABLE.map(row => (
                  <tr key={row.size} className={`border-b border-slate-700/50 ${size === row.size ? 'bg-blue-900/20' : ''}`}>
                    <td className="py-1.5 text-white font-medium">{row.size}P</td>
                    <td className="py-1.5 text-right text-emerald-400">${row.usd}</td>
                    <td className="py-1.5 text-right text-slate-300">{WEIGHT_MAP[row.size] ?? '-'}</td>
                    <td className="py-1.5 pl-3 text-slate-400">{row.note}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p className="text-base text-slate-500 mt-2">※中国輸送費単価: {CHINA_FREIGHT_PER_KG}円/kg（ルミエール日向32BOX×2実績）</p>
          </div>

          {/* 計算フォーム */}
          <div className="bg-slate-800 border border-slate-700 rounded-2xl p-5">
            <p className="text-base font-semibold text-white mb-4">🧮 粗利シミュレーター</p>
            <div className="grid grid-cols-2 gap-3 mb-4">
              <div>
                <label className="text-base text-slate-400 mb-1 block">USD/JPYレート</label>
                <input type="number" value={rate} onChange={e => setRate(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white text-base focus:outline-none focus:border-blue-500" />
              </div>
              <div>
                <label className="text-base text-slate-400 mb-1 block">BOXサイズ</label>
                <select value={size} onChange={e => setSize(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white text-base focus:outline-none focus:border-blue-500">
                  {PRICE_TABLE.map(p => <option key={p.size} value={p.size}>{p.size}P</option>)}
                </select>
              </div>
              <div>
                <label className="text-base text-slate-400 mb-1 block">本体USD（上書き）</label>
                <input type="number" value={customUsd} onChange={e => setCustomUsd(e.target.value)}
                  placeholder={`${priceRow.usd} (デフォルト)`}
                  className="w-full px-3 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white text-base focus:outline-none focus:border-blue-500 placeholder-slate-600" />
              </div>
              <div>
                <label className="text-base text-slate-400 mb-1 block">重量kg（上書き）</label>
                <input type="number" value={customWeight} onChange={e => setCustomWeight(e.target.value)}
                  placeholder={`${WEIGHT_MAP[size] ?? 80} (デフォルト)`}
                  className="w-full px-3 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white text-base focus:outline-none focus:border-blue-500 placeholder-slate-600" />
              </div>
              <div className="col-span-2">
                <label className="text-base text-slate-400 mb-1 block">JITBOX（国内輸送）</label>
                <select value={jitboxPreset} onChange={e => setJitboxPreset(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white text-base focus:outline-none focus:border-blue-500 mb-2">
                  {JITBOX_PRESETS.map((p, i) => (
                    <option key={i} value={i}>{p.label}{p.cost ? `（${p.cost.toLocaleString()}円）` : ''}</option>
                  ))}
                </select>
                {jitboxPreset === JITBOX_PRESETS.length - 1 && (
                  <input type="number" value={jitboxCustom} onChange={e => setJitboxCustom(e.target.value)}
                    placeholder="カスタム金額（円）"
                    className="w-full px-3 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white text-base focus:outline-none focus:border-blue-500" />
                )}
              </div>
              <div>
                <label className="text-base text-slate-400 mb-1 block">請求金額（円）</label>
                <input type="number" value={revenue} onChange={e => setRevenue(Number(e.target.value))}
                  className="w-full px-3 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white text-base focus:outline-none focus:border-blue-500" />
              </div>
            </div>

            {/* 計算結果 */}
            <div className="bg-slate-900 rounded-xl p-4 text-base space-y-1.5">
              <div className="flex justify-between text-slate-300">
                <span>本体（{usd}USD × {rate}円）</span>
                <span>{body.toLocaleString()}円</span>
              </div>
              <div className="flex justify-between text-slate-300">
                <span>中国輸送費（{weight}kg × {CHINA_FREIGHT_PER_KG}円）</span>
                <span>{freight.toLocaleString()}円</span>
              </div>
              <div className="flex justify-between text-slate-300">
                <span>JITBOX</span>
                <span>{jitboxCost.toLocaleString()}円</span>
              </div>
              <div className="flex justify-between text-white font-semibold border-t border-slate-700 pt-2">
                <span>発注金額合計</span>
                <span>{total.toLocaleString()}円</span>
              </div>
              <div className="flex justify-between text-white font-semibold">
                <span>請求金額</span>
                <span>{revenue.toLocaleString()}円</span>
              </div>
              <div className={`flex justify-between font-bold text-base border-t border-slate-700 pt-2 ${profit < 0 ? 'text-red-400' : 'text-emerald-400'}`}>
                <span>粗利益</span>
                <span>{profit < 0 ? '▲' : ''}{Math.abs(profit).toLocaleString()}円{profit < 0 ? '（赤字）' : ''}</span>
              </div>
            </div>

            {/* 案件追加 */}
            <div className="mt-4 border-t border-slate-700 pt-4">
              <p className="text-base text-slate-400 mb-2">承認メール用に案件を追加</p>
              <div className="grid grid-cols-2 gap-2 mb-2">
                <input value={company} onChange={e => setCompany(e.target.value)} placeholder="企業名"
                  className="px-3 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white text-base focus:outline-none focus:border-emerald-500 placeholder-slate-600" />
                <input value={property} onChange={e => setProperty(e.target.value)} placeholder="物件名"
                  className="px-3 py-2 bg-slate-900 border border-slate-600 rounded-lg text-white text-base focus:outline-none focus:border-emerald-500 placeholder-slate-600" />
              </div>
              <div className="flex gap-3 mb-3 text-base">
                <label className="flex items-center gap-1.5 text-slate-300 cursor-pointer">
                  <input type="checkbox" checked={paid} onChange={e => setPaid(e.target.checked)} className="accent-emerald-500" />
                  入金済み
                </label>
                <label className="flex items-center gap-1.5 text-slate-300 cursor-pointer">
                  <input type="checkbox" checked={exception} onChange={e => setException(e.target.checked)} className="accent-orange-500" />
                  旧料金例外適用
                </label>
              </div>
              <button onClick={addItem} disabled={!company || !property}
                className="w-full py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-40 disabled:cursor-not-allowed text-white text-base font-medium rounded-lg transition-colors">
                ＋ 案件を追加
              </button>
            </div>
          </div>

          {/* 追加済み案件リスト */}
          {items.length > 0 && (
            <div className="bg-slate-800 border border-slate-700 rounded-2xl p-5">
              <div className="flex items-center justify-between mb-3">
                <p className="text-base font-semibold text-white">追加案件（{items.length}件）</p>
                <button onClick={genMail}
                  className="px-4 py-1.5 bg-blue-600 hover:bg-blue-500 text-white text-base font-medium rounded-lg transition-colors">
                  📧 承認メール生成
                </button>
              </div>
              <div className="space-y-2">
                {items.map((it, i) => (
                  <div key={i} className="flex items-center justify-between bg-slate-900 rounded-lg px-3 py-2 text-base">
                    <div>
                      <span className="text-white font-medium">{it.company} / {it.property}</span>
                      <span className="text-slate-400 text-base ml-2">{it.size}P　発注:{it.cost.toLocaleString()}円　粗利:{it.profit < 0 ? '▲' : ''}{Math.abs(it.profit).toLocaleString()}円</span>
                      {it.exception && <span className="ml-2 text-base text-orange-400">旧料金</span>}
                      {!it.paid && <span className="ml-2 text-base text-yellow-400">未入金</span>}
                    </div>
                    <button onClick={() => removeItem(i)} className="text-slate-500 hover:text-red-400 text-base ml-3">✕</button>
                  </div>
                ))}
              </div>

              {mailText && (
                <div className="mt-4 bg-slate-900 border border-slate-600 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-base text-slate-400">社長承認メール</span>
                    <button onClick={() => { navigator.clipboard.writeText(mailText); setMailCopied(true); setTimeout(() => setMailCopied(false), 2000) }}
                      className="px-3 py-1 text-base text-slate-400 hover:text-white border border-slate-600 rounded-lg transition-colors">
                      {mailCopied ? '✅ コピー済み' : '📋 コピー'}
                    </button>
                  </div>
                  <pre className="text-slate-200 text-base whitespace-pre-wrap leading-relaxed font-sans">{mailText}</pre>
                </div>
              )}
            </div>
          )}
        </div>

        {/* 右：発注フロー */}
        <div className="bg-slate-800 border border-slate-700 rounded-2xl p-5">
          <p className="text-base font-semibold text-white mb-4">🔄 キーボックス発注フロー</p>
          <div className="space-y-4">
            {FLOW_STEPS.map(s => (
              <div key={s.step} className="flex gap-3">
                <div className="flex-shrink-0 w-7 h-7 bg-blue-700 rounded-full flex items-center justify-center text-sm font-bold text-white">
                  {s.step}
                </div>
                <div className="flex-1 pb-4 border-b border-slate-700/50">
                  <p className="text-white text-base font-medium mb-1">{s.title}</p>
                  <p className="text-slate-400 text-base leading-relaxed whitespace-pre-line">{s.detail}</p>
                </div>
              </div>
            ))}
          </div>

          {/* 承認メールテンプレ */}
          <div className="mt-5 bg-slate-900 rounded-xl p-4">
            <p className="text-base font-medium text-slate-300 mb-2">📝 社長承認メール 件名フォーマット</p>
            <code className="text-base text-emerald-300">※田中社長確認 キーボックス発注依頼YYYYMMDD</code>
            <p className="text-base text-slate-500 mt-2">
              ※旧料金例外の場合は必ず本文に明記<br />
              ※発注金額・請求金額・粗利を全案件分記載<br />
              ※入金前発注の場合は理由を記載（12月納品希望・輸送費圧縮など）
            </p>
          </div>

          {/* 寸法メモ */}
          <div className="mt-4 bg-slate-900 rounded-xl p-4">
            <p className="text-base font-medium text-slate-300 mb-2">📐 機器寸法メモ</p>
            <div className="space-y-2 text-base text-slate-400">
              <div>
                <span className="text-slate-300 font-medium">KIOSK（CKM3 現行縦置き型）</span><br />
                W: 574.3mm　H: 1,454mm（本体）　D: 630mm（ベース含む）
              </div>
              <div>
                <span className="text-slate-300 font-medium">キーボックス 28BOX（7×4）</span><br />
                W: 約700mm　H: 約1,800mm　D: 約600mm
              </div>
              <p className="text-yellow-400 mt-1">⚠️ KIOSK + キーボックス 並列設置は2m以内に収まるか要確認</p>
            </div>
          </div>
        </div>

      </div>
    </div>
  )
}
