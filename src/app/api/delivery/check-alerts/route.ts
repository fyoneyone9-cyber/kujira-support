import { createClient } from '@supabase/supabase-js'
import { NextRequest, NextResponse } from 'next/server'

export const runtime = 'nodejs'

// Vercel Cron または手動で叩く納品アラートのSlack通知
// vercel.json に以下を追加して毎朝自動実行する想定：
// { "path": "/api/delivery/check-alerts", "schedule": "0 0 * * 1-5" }  (JST 9:00 = UTC 0:00)

type EquipmentItem = { name: string; value: string }
type Row = {
  id: string
  client_name: string
  product_name: string
  assignee: string
  delivery_due_date: string
  progress: string
  equipment: EquipmentItem[] | null
  manual_ordered: string[] | null
  p400_status: string | null
  paycube_status: string | null
  vega3000_status: string | null
  equipment_arrival_dates: Record<string, string> | null
}

const LEAD_TIME_DAYS: { match: RegExp; days: number; label: string }[] = [
  { match: /P400/i, days: 60, label: 'P400' },
  { match: /PayCube|ペイキューブ/i, days: 50, label: 'PayCube' },
  { match: /VEGA3000|ベガ3000/i, days: 45, label: 'VEGA3000' },
  { match: /キーボックス/i, days: 60, label: 'キーボックス' },
  { match: /卓上KIOSK|卓上キオスク/i, days: 30, label: '卓上KIOSK' },
  { match: /KIOSK|キオスク/i, days: 30, label: 'KIOSK' },
  { match: /パスポートリーダー/i, days: 30, label: 'パスポートリーダー' },
]

function daysLeft(dueDate: string): number {
  const today = new Date(); today.setHours(0, 0, 0, 0)
  const due = new Date(dueDate)
  return Math.ceil((due.getTime() - today.getTime()) / 86400000)
}

// 案件全体として最もリスクが高い（小さい）猶予日数を計算する。
// ・機器ごとに「商品到着予定日」が入っていればそれを最優先（納品予定日 - 到着予定日）
// ・到着予定日未入力かつ発注済みチェック済みなら安全（null）扱いで除外
// ・未発注ならリードタイム推定値で判定
// 機器が1つも無い案件は null を返す（呼び出し側で daysLeft を使う）
function getRiskiestBuffer(row: Row): number | null {
  const names: string[] = []
  if (row.equipment) names.push(...row.equipment.map(e => e.name))
  if (row.product_name) names.push(row.product_name)
  const ordered = row.manual_ordered || []
  const arrivals = row.equipment_arrival_dates || {}

  const matchedLabels = LEAD_TIME_DAYS.filter(lt => names.some(n => lt.match.test(n)))
  if (matchedLabels.length === 0) return null

  const buffers: number[] = []
  for (const lt of matchedLabels) {
    const arrival = arrivals[lt.label]
    if (arrival) {
      const due = new Date(row.delivery_due_date); due.setHours(0, 0, 0, 0)
      const arr = new Date(arrival); arr.setHours(0, 0, 0, 0)
      buffers.push(Math.ceil((due.getTime() - arr.getTime()) / 86400000))
      continue
    }
    if (ordered.includes(lt.label)) continue // 発注済み・到着日未入力 → 除外（安全扱い）
    buffers.push(daysLeft(row.delivery_due_date) - lt.days)
  }
  if (buffers.length === 0) return null
  return Math.min(...buffers)
}

export async function GET(req: NextRequest) {
  const authHeader = req.headers.get('authorization')
  if (
    process.env.CRON_SECRET &&
    authHeader !== `Bearer ${process.env.CRON_SECRET}`
  ) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  )

  const { data, error } = await supabase
    .from('delivery_items')
    .select('id, client_name, product_name, assignee, delivery_due_date, progress, equipment, manual_ordered, p400_status, paycube_status, vega3000_status, equipment_arrival_dates')
    .eq('status', 'active')
    .order('delivery_due_date', { ascending: true })

  if (error) return NextResponse.json({ error: error.message }, { status: 500 })

  const rows = (data || []) as Row[]

  const overdue: { row: Row; buffer: number }[] = []
  const critical: { row: Row; buffer: number }[] = []
  const urgent: { row: Row; buffer: number }[] = []
  // 「納品日の前日」専用アラーム：発注猶予（機器リードタイム）とは無関係に、
  // 実際の納品予定日がちょうど明日（残り1日）の案件を必ず拾う。
  const dueTomorrow: Row[] = []

  for (const row of rows) {
    const riskiest = getRiskiestBuffer(row)
    // 機器が無い案件、または全機器が「発注済み・到着日未入力＝安全」なら納品予定日ベースで判定。
    // 機器があり到着予定日やリードタイムから危険度が出ている場合はそちらを優先する。
    const buffer = riskiest !== null ? riskiest : daysLeft(row.delivery_due_date)
    if (buffer < 0) overdue.push({ row, buffer })
    else if (buffer <= 3) critical.push({ row, buffer })
    else if (buffer <= 7) urgent.push({ row, buffer })

    if (daysLeft(row.delivery_due_date) === 1) dueTomorrow.push(row)
  }

  const slackWebhook = process.env.DELIVERY_SLACK_WEBHOOK_URL || process.env.SLACK_WEBHOOK_URL

  if (slackWebhook && dueTomorrow.length > 0) {
    const lines: string[] = []
    lines.push('⏰🔔 *【納品前日アラーム】明日が納品予定日の案件：' + dueTomorrow.length + '件*')
    dueTomorrow.forEach(row => {
      const who = row.assignee ? `担当: ${row.assignee}` : '担当: 未設定'
      lines.push(`• ${row.client_name}（${row.product_name || '製品名未設定'}） / 納品予定日: ${row.delivery_due_date}（明日！） / 進捗: ${row.progress || '未設定'} / ${who}`)
    })
    lines.push('')
    lines.push('📋 最終確認・準備物チェック: https://support.nextralab.jp/delivery')
    await fetch(slackWebhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: lines.join('\n') })
    }).catch(() => {})
  }

  if (slackWebhook && (overdue.length > 0 || critical.length > 0 || urgent.length > 0)) {
    const lines: string[] = []
    lines.push('📦 *IoT製品 納品予定アラート*')
    lines.push(`📅 チェック日: ${new Date().toLocaleDateString('ja-JP')}`)
    lines.push('')

    const fmt = (row: Row, buffer: number) => {
      const who = row.assignee ? `担当: ${row.assignee}` : '担当: 未設定'
      const bufferText = buffer < 0 ? `${-buffer}日超過` : `残${buffer}日`
      return `• ${row.client_name}（${row.product_name || '製品名未設定'}） / 納品予定: ${row.delivery_due_date} / 発注猶予: ${bufferText} / ${who}`
    }

    if (overdue.length > 0) {
      lines.push(`🚨 *【期限超過】今すぐ発注しても間に合わない：${overdue.length}件*`)
      overdue.forEach(({ row, buffer }) => lines.push(fmt(row, buffer)))
      lines.push('')
    }
    if (critical.length > 0) {
      lines.push(`🔴 *【緊急】発注猶予3日以内：${critical.length}件*`)
      critical.forEach(({ row, buffer }) => lines.push(fmt(row, buffer)))
      lines.push('')
    }
    if (urgent.length > 0) {
      lines.push(`🟠 *【要対応】発注猶予1週間以内：${urgent.length}件*`)
      urgent.forEach(({ row, buffer }) => lines.push(fmt(row, buffer)))
      lines.push('')
    }

    lines.push('📋 詳細・発注済みチェック: https://support.nextralab.jp/delivery')

    await fetch(slackWebhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: lines.join('\n') })
    }).catch(() => {})
  }

  return NextResponse.json({
    ok: true,
    overdue: overdue.length,
    critical: critical.length,
    urgent: urgent.length,
    due_tomorrow: dueTomorrow.length,
    slack_sent: !!slackWebhook,
  })
}
