# -*- coding: utf-8 -*-
"""
delivery/page.tsx への全変更を一括適用するパッチスクリプト
1. React import追加
2. jitbox_ordered フィールドをDeliveryItem型に追加
3. JITBOXヘルパー関数追加
4. getAlertReason をJSX返しに書き換え
5. toggleJitboxOrdered 関数追加
6. カード内表示変更（getAlertReason -> div, JITBOXブロック追加, 管理スプレッドシートボタン追加）
"""
import re

path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# ---- 1. React import ----
content = content.replace(
    "import { useEffect, useState } from 'react'",
    "import React, { useEffect, useState } from 'react'"
)

# ---- 2. jitbox_ordered フィールド追加 ----
content = content.replace(
    "  worker_contacts?: { name: string; tel: string; email: string }[] | null\n}",
    "  worker_contacts?: { name: string; tel: string; email: string }[] | null\n  jitbox_ordered?: boolean | null\n}"
)

# ---- 3. JITBOXヘルパー関数（LEAD_TIME_DAYS の直前に挿入） ----
jitbox_helpers = '''\n// JITBOXチャーター便の検出と大阪発リードタイム計算
// 備考(notes)または製品名(product_name)に「JITBOX」「JITボックス」が含まれる場合に表示
function hasJitbox(it: { notes?: string; product_name?: string }): boolean {
  const text = `${it.notes || ''} ${it.product_name || ''}`.toLowerCase()
  return /jitbox|jitボックス|jit ボックス/.test(text)
}

// 大阪発のJITBOX所要日数（900km基準）
function getJitboxLeadDays(installAddress: string): { days: number; note: string } {
  const addr = installAddress || ''
  if (/北海道|青森|岩手|秋田|沖縄|離島/.test(addr)) {
    return { days: 2, note: '大阪→当地 約900km超のため翌々日（日祝またぎは+1日）' }
  }
  if (/宮城|山形|福島/.test(addr)) {
    return { days: 2, note: '大阪→東北 約900km前後のため翌々日' }
  }
  return { days: 1, note: '大阪→当地 900km圏内のため翌日（目安）' }
}

'''

content = content.replace('const LEAD_TIME_DAYS', jitbox_helpers + 'const LEAD_TIME_DAYS', 1)

# ---- 4. getAlertReason を JSX返しに書き換え ----
old_fn = '''function getAlertReason(it: DeliveryItem): string {
  const allMatched = getMatchedEquipment(it)
  const plain = daysLeft(it.delivery_due_date)
  const who = it.assignee ? `担当の${it.assignee}さん` : '担当者'

  if (allMatched.length > 0) {
    // 各機器の状態を分類
    const withArrival = allMatched
      .map(m => ({ m, arrival: getArrivalDate(it, m.label), buffer: getEquipmentBuffer(it.delivery_due_date, it, m) }))
    const risky = withArrival.filter(w => w.buffer !== null).sort((a, b) => (a.buffer as number) - (b.buffer as number))
    const safe = withArrival.filter(w => w.buffer === null) // 到着日未入力の発注済み機器

    // 全機器が「安全」（到着日未入力の発注済みのみ）→ 到着日の入力を促す
    if (risky.length === 0) {
      const names = safe.map(w => w.m.label).join('・')
      return `${it.client_name}の${names}は発注済みですが、商品到着予定日が未入力です。納品予定日（${it.delivery_due_date}）まであと${plain}日なので、メーカー・仕入先から届いた到着予定日をダッシュボードに入力してください。`
    }

    const main = risky[0]
    const buffer = main.buffer as number

    const statusNote = main.arrival
      ? `（商品到着予定日：${main.arrival}）`
      : (() => {
          const s = getArrangementStatus(it, main.m.label)
          return s ? `（現在の手配状況：${s}）` : '（手配状況・到着予定日とも未入力のため要確認）'
        })()

    const othersParts: string[] = []
    const othersRisky = risky.slice(1)
    if (othersRisky.length > 0) {
      othersParts.push(`他にも${othersRisky.map(w => `${w.m.label}（猶予${w.buffer}日）`).join('・')}も要確認です。`)
    }
    if (safe.length > 0) {
      othersParts.push(`${safe.map(w => w.m.label).join('・')}は発注済み（到着予定日は未入力）です。`)
    }
    const othersText = othersParts.join('')

    const arrivalPhrase = main.arrival
      ? `到着予定日（${main.arrival}）が納品予定日（${it.delivery_due_date}）`
      : `${main.m.label}は発注〜納品に約${main.m.days}日かかり、納品予定日（${it.delivery_due_date}）`

    if (buffer < 0) {
      return main.arrival
        ? `${it.client_name}の${main.m.label}は到着予定日（${main.arrival}）が納品予定日（${it.delivery_due_date}）より${-buffer}日遅く、このままでは間に合いません。${who}が仕入先に納期前倒しを相談するか、お客様に納品予定日の再調整を相談してください。${othersText}`
        : `${it.client_name}の${main.m.label}は発注〜納品に約${main.m.days}日かかるのに、納品予定日まであと${plain}日しかなく、今日発注しても${-buffer}日間に合いません${statusNote}。${who}がすでに発注済みか、未発注なら至急発注するか、お客様に納期の再調整を相談してください。${othersText}`
    }
    if (buffer <= 3) {
      return `${arrivalPhrase}まであと${buffer}日しか余裕がありません${statusNote}。${who}に状況を今すぐ確認してください。${othersText}`
    }
    if (buffer <= 7) {
      return `${arrivalPhrase}まで余裕は${buffer}日です${statusNote}。今週中に${who}が状況を確認してください。${othersText}`
    }
    if (buffer <= 14) {
      return `${arrivalPhrase}まで余裕は${buffer}日あります${statusNote}。念のため${who}に状況を確認しておいてください。${othersText}`
    }
    return `${arrivalPhrase}まで余裕は${buffer}日あるので今は様子見で問題ありません${statusNote}。${othersText}`
  }

  // リードタイム不要（設定・確認系タスク等）
  const progressNote = it.progress ? `現在の進捗は「${it.progress}」です。` : ''
  if (plain < 0) {
    return `${it.client_name}の案件（${it.product_name || '対応タスク'}）は納品予定日（${it.delivery_due_date}）を${-plain}日過ぎています。${progressNote}${who}に進捗状況と遅延理由をすぐ確認してください。`
  }
  if (plain <= 3) {
    return `${it.client_name}の案件（${it.product_name || '対応タスク'}）は納品予定日（${it.delivery_due_date}）まであと${plain}日です。${progressNote}${who}に準備（設定・動作確認・訪問調整等）が完了しているか確認してください。`
  }
  if (plain <= 7) {
    return `${it.client_name}の案件（${it.product_name || '対応タスク'}）は納品予定日まであと${plain}日です。${progressNote}今週中に${who}に対応状況を確認してください。`
  }
  return `${it.client_name}の案件（${it.product_name || '対応タスク'}）は納品予定日まであと${plain}日あります。${progressNote}余裕はありますが念のため進捗を確認しておいてください。`
}'''

new_fn = '''function getAlertReason(it: DeliveryItem): React.ReactNode {
  const allMatched = getMatchedEquipment(it)
  const plain = daysLeft(it.delivery_due_date)
  const who = it.assignee ? `担当：${it.assignee}さん` : '担当者'

  if (allMatched.length > 0) {
    const withArrival = allMatched.map(m => ({
      m,
      arrival: getArrivalDate(it, m.label),
      buffer: getEquipmentBuffer(it.delivery_due_date, it, m),
      ordered: isManuallyOrdered(it, m.label),
      status: getArrangementStatus(it, m.label),
    }))
    const risky = withArrival.filter(w => w.buffer !== null).sort((a, b) => (a.buffer as number) - (b.buffer as number))
    const safe = withArrival.filter(w => w.buffer === null)

    if (risky.length === 0) {
      const names = safe.map(w => w.m.label).join('・')
      return (
        <div className="space-y-1">
          <p>📦 <strong>{names}</strong> は発注済みですが、<span className="text-yellow-300 font-bold">商品到着予定日が未入力</span>です。</p>
          <p>📅 納品予定日 <strong>{it.delivery_due_date}</strong>（残 {plain}日）</p>
          <p>✏️ メーカー・仕入先から届いた到着予定日をダッシュボードに入力してください。</p>
        </div>
      )
    }

    const equipRows = withArrival.map(w => {
      const buf = w.buffer
      const bufText = buf === null
        ? <span className="text-green-300">発注済み（到着日未入力）</span>
        : buf < 0
          ? <span className="text-red-300 font-bold">{-buf}日超過（間に合わない）</span>
          : buf <= 3
            ? <span className="text-red-300 font-bold">残{buf}日（今すぐ対応）</span>
            : buf <= 7
              ? <span className="text-orange-300 font-bold">残{buf}日（今週中）</span>
              : buf <= 14
                ? <span className="text-yellow-300 font-bold">残{buf}日（要確認）</span>
                : <span className="text-green-300">残{buf}日（余裕あり）</span>
      const arrivalText = w.arrival
        ? <span>到着予定 <strong>{w.arrival}</strong></span>
        : w.ordered
          ? <span className="text-slate-400">発注済み・到着日未入力</span>
          : w.status
            ? <span className="text-slate-400">手配状況：{w.status}</span>
            : <span className="text-red-400 font-bold">未発注・到着日未入力</span>
      return (
        <li key={w.m.label} className="flex flex-wrap gap-2 items-center text-base">
          <span className="font-bold text-white min-w-[8rem]">📦 {w.m.label}</span>
          <span className="text-slate-400 text-sm">（リードタイム約{w.m.days}日）</span>
          <span>{arrivalText}</span>
          <span className="text-slate-500">｜</span>
          <span>発注猶予：{bufText}</span>
        </li>
      )
    })

    const mainBuffer = risky[0].buffer as number
    const actions: string[] = []
    if (mainBuffer < 0) {
      if (risky[0].arrival) {
        actions.push('仕入先に納期前倒しを交渉する')
        actions.push('お客様に納品予定日の再調整を相談する')
      } else {
        actions.push('発注済みか今すぐ確認（未発注なら至急発注）')
        actions.push('今日発注しても間に合わないため、お客様に納期再調整を相談する')
      }
    } else if (mainBuffer <= 3) {
      actions.push('今すぐ発注状況を確認・発注を完了させる')
      actions.push('到着予定日をダッシュボードに入力する')
    } else if (mainBuffer <= 7) {
      actions.push('今週中に発注状況を確認する')
      actions.push('到着予定日をダッシュボードに入力する')
    } else {
      actions.push('念のため発注状況・到着予定日を確認する')
    }
    if (safe.length > 0) {
      actions.push(`${safe.map(w => w.m.label).join('・')} の到着予定日をダッシュボードに入力する`)
    }

    return (
      <div className="space-y-2 text-base">
        <div className="flex flex-wrap gap-3 text-slate-300">
          <span>📅 納品予定日 <strong className="text-white">{it.delivery_due_date}</strong>（残 {plain}日）</span>
          <span>👤 {who}</span>
          {it.progress && <span>📋 進捗：{it.progress}</span>}
        </div>
        <ul className="space-y-1 pl-1 border-l-2 border-slate-600">
          {equipRows}
        </ul>
        <div className="mt-1 pt-1 border-t border-slate-700">
          <p className="text-slate-400 text-sm font-bold mb-1">🔴 今すぐやること：</p>
          <ul className="space-y-0.5 pl-3">
            {actions.map((a, i) => <li key={i} className="text-yellow-200 text-sm">▶ {a}</li>)}
          </ul>
        </div>
      </div>
    )
  }

  const progressNote = it.progress ? `進捗：「${it.progress}」` : ''
  let summary = ''
  let actionText = ''
  if (plain < 0) {
    summary = `納品予定日（${it.delivery_due_date}）を ${-plain}日 超過しています。`
    actionText = '進捗状況と遅延理由を今すぐ確認してください。'
  } else if (plain <= 3) {
    summary = `納品予定日（${it.delivery_due_date}）まであと ${plain}日 です。`
    actionText = '設定・動作確認・訪問調整等が完了しているか確認してください。'
  } else if (plain <= 7) {
    summary = `納品予定日まであと ${plain}日 です。`
    actionText = '今週中に対応状況を確認してください。'
  } else {
    summary = `納品予定日まであと ${plain}日 あります。`
    actionText = '念のため進捗を確認しておいてください。'
  }
  return (
    <div className="space-y-1 text-base">
      <p>📅 {summary}</p>
      {progressNote && <p className="text-slate-400">{progressNote}</p>}
      <p>👤 {who} ▶ {actionText}</p>
    </div>
  )
}'''

if old_fn in content:
    content = content.replace(old_fn, new_fn, 1)
    print('getAlertReason replaced OK')
else:
    print('ERROR: getAlertReason not found')

# ---- 5. toggleJitboxOrdered 関数追加（saveWorkDate の直前） ----
toggle_fn = '''
  const toggleJitboxOrdered = async (it: DeliveryItem) => {
    if (blockIfLocked(it)) return
    const next = !it.jitbox_ordered
    const msg = next
      ? `「${it.client_name}」のJITBOX手配を「手配済み」にしますか？`
      : `「${it.client_name}」のJITBOX手配を「未手配」に戻しますか？`
    if (!window.confirm(msg)) return
    setItems(prev => prev.map(p => p.id === it.id ? { ...p, jitbox_ordered: next } : p))
    await fetch('/api/delivery/items', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: it.id, jitbox_ordered: next })
    })
  }

  // 作業日を保存'''

content = content.replace('  // 作業日を保存', toggle_fn, 1)
print('toggleJitboxOrdered inserted OK')

# ---- 6a. バナー内 getAlertReason の <p> を <div> に ----
content = content.replace(
    '<p className="text-base text-red-200 leading-relaxed">👉 {getAlertReason(it)}</p>',
    '<div className="text-base text-red-200 leading-relaxed">{getAlertReason(it)}</div>'
)
content = content.replace(
    '<p className="text-base text-orange-200 leading-relaxed">👉 {getAlertReason(it)}</p>',
    '<div className="text-base text-orange-200 leading-relaxed">{getAlertReason(it)}</div>'
)

# ---- 6b. カード内 getAlertReason の <p> を <div> に ----
content = content.replace(
    '                        <p className="text-base bg-black/20 rounded-lg px-3 py-2 mt-1 leading-relaxed">\n                          👉 {getAlertReason(it)}\n                        </p>',
    '                        <div className="text-base bg-black/20 rounded-lg px-3 py-2 mt-1 leading-relaxed">\n                          {getAlertReason(it)}\n                        </div>'
)

# ---- 6c. JITBOXブロックを作業員セクションの直前に挿入 ----
jitbox_block = '''                      {/* JITBOX配送情報（備考にJITBOXが含まれる場合） */}
                      {hasJitbox(it) && (() => {
                        const jit = getJitboxLeadDays(it.install_address)
                        const _today = new Date(); _today.setHours(0, 0, 0, 0)
                        const _due = new Date(it.delivery_due_date); _due.setHours(0, 0, 0, 0)
                        const _deadline = new Date(_due)
                        _deadline.setDate(_deadline.getDate() - jit.days - 1)
                        const deadlineStr = _deadline.toISOString().slice(0, 10)
                        const daysToDeadline = Math.ceil((_deadline.getTime() - _today.getTime()) / 86400000)
                        const isOverdue = daysToDeadline < 0
                        const isUrgent = !isOverdue && daysToDeadline <= 3
                        return (
                          <div className={`flex flex-col gap-2 mt-2 pt-2 border-t ${isOverdue ? 'border-red-500' : isUrgent ? 'border-orange-500' : 'border-slate-700/50'}`}>
                            <div className={`flex flex-col gap-1.5 px-3 py-2 rounded-lg ${isOverdue ? 'bg-red-950/50 border border-red-500' : isUrgent ? 'bg-orange-950/50 border border-orange-500' : 'bg-slate-800/60 border border-slate-700'}`}>
                              <div className="flex items-center gap-2 flex-wrap">
                                <span className="text-lg font-bold text-white">🚚 JITBOX配送情報（大阪発）</span>
                                {isOverdue && <span className="text-sm px-2 py-0.5 rounded-full bg-red-600 text-white font-bold">手配期限超過！</span>}
                                {isUrgent && <span className="text-sm px-2 py-0.5 rounded-full bg-orange-500 text-white font-bold">手配期限まで{daysToDeadline}日</span>}
                              </div>
                              <div className="text-base text-slate-300 space-y-0.5">
                                <p>📦 所要日数：<strong className="text-white">{jit.days}日</strong> <span className="text-slate-400 text-sm">（{jit.note}）</span></p>
                                <p>⏰ 手配締め切り：
                                  <strong className={isOverdue ? 'text-red-300' : isUrgent ? 'text-orange-300' : 'text-white'}> {deadlineStr}</strong>
                                  <span className="text-slate-400 ml-2 text-sm">（{isOverdue ? `${-daysToDeadline}日超過` : `残${daysToDeadline}日`} ／ 前日までに手配必要）</span>
                                </p>
                                <p className="text-slate-400 text-sm">⚠️ 日祝またぎ・離島・2時間幅JIT指定は別途確認。時間外配達(18:01〜20:00)は+3,000円前後。</p>
                              </div>
                              <button
                                onClick={() => toggleJitboxOrdered(it)}
                                disabled={!!it.locked}
                                className={`self-start text-base px-4 py-1.5 rounded-full font-bold border transition-colors whitespace-nowrap ${it.jitbox_ordered ? 'bg-green-700 border-green-500 text-white' : 'bg-slate-700/60 border-slate-600 text-slate-300 hover:bg-slate-600'} ${it.locked ? 'opacity-50 cursor-not-allowed' : ''}`}
                              >
                                {it.jitbox_ordered ? '✅ JITBOX手配済み' : '☐ JITBOX手配済みにする'}
                              </button>
                            </div>
                          </div>
                        )
                      })()}

'''

worker_section = '                      {/* 作業員管理：必要/不要・作業日・連絡先（複数人登録可） */}'
if worker_section in content:
    content = content.replace(worker_section, jitbox_block + worker_section, 1)
    print('JITBOX JSX block inserted OK')
else:
    print('ERROR: worker section marker not found')

# ---- 6d. 管理スプレッドシートボタンを各カード右側ボタン列（工程管理表の下）に追加 ----
mgmt_btn = '''                      <a
                        href="https://docs.google.com/spreadsheets/d/1GiEvK-KLB7rl1lrCn-Llgl9H6W4m2PuZJXby2RqIuMc/edit?gid=602309486#gid=602309486"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-base rounded-lg font-medium transition-colors whitespace-nowrap text-center"
                      >
                        🛠️ 工程管理表
                      </a>
                      <a
                        href="https://docs.google.com/spreadsheets/d/1FxK4x534LV2sGY54KKtbow1W6iLT0Z_YTzg_R8ba8Go/edit?gid=0#gid=0"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-4 py-2 bg-green-700 hover:bg-green-600 text-white text-base rounded-lg font-medium transition-colors whitespace-nowrap text-center"
                      >
                        📊 管理スプレッドシート
                      </a>
                      <button
                        onClick={() => markChecked(it)}'''

old_btn = '''                      <a
                        href="https://docs.google.com/spreadsheets/d/1GiEvK-KLB7rl1lrCn-Llgl9H6W4m2PuZJXby2RqIuMc/edit?gid=602309486#gid=602309486"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-base rounded-lg font-medium transition-colors whitespace-nowrap text-center"
                      >
                        🛠️ 工程管理表
                      </a>
                      <button
                        onClick={() => markChecked(it)}'''

if old_btn in content:
    content = content.replace(old_btn, mgmt_btn, 1)
    print('Management spreadsheet button added OK')
else:
    print('ERROR: button target not found')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print('\nAll patches applied.')
