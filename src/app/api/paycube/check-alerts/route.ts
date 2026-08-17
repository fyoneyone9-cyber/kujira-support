import { createClient } from '@supabase/supabase-js'
import { NextRequest, NextResponse } from 'next/server'

export const runtime = 'nodejs'

// Vercel Cron または手動で叩くアラートチェック
// vercel.json に "cron": [{"path": "/api/paycube/check-alerts", "schedule": "0 9 * * 1-5"}] を追加
export async function GET(req: NextRequest) {
  // cronシークレット確認
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

  const today = new Date()
  const twoMonthsLater = new Date(today)
  twoMonthsLater.setMonth(twoMonthsLater.getMonth() + 2)
  const oneMonthLater = new Date(today)
  oneMonthLater.setMonth(oneMonthLater.getMonth() + 1)
  const twoWeeksLater = new Date(today)
  twoWeeksLater.setDate(twoWeeksLater.getDate() + 14)

  // 2ヶ月以内に期限が来る契約を取得
  const { data: contracts } = await supabase
    .from('paycube_contracts')
    .select('*')
    .neq('status', 'expired')
    .neq('status', 'renewed')
    .lte('end_date', twoMonthsLater.toISOString().split('T')[0])
    .gte('end_date', today.toISOString().split('T')[0])
    .order('end_date', { ascending: true })

  if (!contracts || contracts.length === 0) {
    return NextResponse.json({ ok: true, message: 'アラート対象なし', count: 0 })
  }

  // 緊急度別に分類
  const critical: typeof contracts = []   // 2週間以内
  const urgent: typeof contracts = []     // 1ヶ月以内
  const warning: typeof contracts = []    // 2ヶ月以内

  for (const c of contracts) {
    const end = new Date(c.end_date)
    if (end <= twoWeeksLater) critical.push(c)
    else if (end <= oneMonthLater) urgent.push(c)
    else warning.push(c)
  }

  // Slack通知
  const slackWebhook = process.env.SLACK_WEBHOOK_URL
  if (slackWebhook) {
    const lines: string[] = []
    lines.push('🚨 *PayCube保守期限アラート*')
    lines.push(`📅 チェック日: ${today.toLocaleDateString('ja-JP')}`)
    lines.push('')

    if (critical.length > 0) {
      lines.push('🔴 *【緊急】2週間以内に期限切れ*')
      for (const c of critical) {
        const daysLeft = Math.ceil((new Date(c.end_date).getTime() - today.getTime()) / 86400000)
        lines.push(`• ${c.client_name} / ${c.plan_name || '不明'} / 期限: ${c.end_date} (残${daysLeft}日)`)
      }
      lines.push('')
    }

    if (urgent.length > 0) {
      lines.push('🟠 *【要対応】1ヶ月以内に期限切れ*')
      for (const c of urgent) {
        const daysLeft = Math.ceil((new Date(c.end_date).getTime() - today.getTime()) / 86400000)
        lines.push(`• ${c.client_name} / ${c.plan_name || '不明'} / 期限: ${c.end_date} (残${daysLeft}日)`)
      }
      lines.push('')
    }

    if (warning.length > 0) {
      lines.push('🟡 *【注意】2ヶ月以内に期限切れ*')
      for (const c of warning) {
        const daysLeft = Math.ceil((new Date(c.end_date).getTime() - today.getTime()) / 86400000)
        lines.push(`• ${c.client_name} / ${c.plan_name || '不明'} / 期限: ${c.end_date} (残${daysLeft}日)`)
      }
      lines.push('')
    }

    lines.push(`📋 詳細: https://support.nextralab.jp/paycube`)

    await fetch(slackWebhook, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: lines.join('\n') })
    }).catch(() => {})
  }

  // statusを 'alerted' に更新（未対応のもの）
  const alertIds = contracts.filter(c => c.status === 'active').map(c => c.id)
  if (alertIds.length > 0) {
    await supabase
      .from('paycube_contracts')
      .update({ status: 'alerted' })
      .in('id', alertIds)
  }

  return NextResponse.json({
    ok: true,
    total: contracts.length,
    critical: critical.length,
    urgent: urgent.length,
    warning: warning.length,
    slack_sent: !!slackWebhook,
  })
}
