import { createClient } from '@supabase/supabase-js'
import { NextRequest, NextResponse } from 'next/server'

export const runtime = 'nodejs'

function parseDate(s: string): string | null {
  if (!s || s === 'None') return null
  const fmts = [
    /^(\d{4})\/(\d{1,2})\/(\d{1,2})/,
    /^(\d{4})-(\d{2})-(\d{2})/,
  ]
  for (const re of fmts) {
    const m = s.match(re)
    if (m) return `${m[1]}-${String(m[2]).padStart(2,'0')}-${String(m[3]).padStart(2,'0')}`
  }
  return null
}

function getCol(row: string[], idx: number): string {
  return (row[idx] || '').trim()
}

export async function POST(req: NextRequest) {
  const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.SUPABASE_SERVICE_ROLE_KEY!
  )

  const formData = await req.formData()
  const file = formData.get('file') as File
  if (!file) return NextResponse.json({ error: 'ファイルがありません' }, { status: 400 })

  const text = await file.text()
  const lines = text.split(/\r?\n/)

  // CSVパース（簡易）
  function parseLine(line: string): string[] {
    const result: string[] = []
    let cur = '', inQ = false
    for (let i = 0; i < line.length; i++) {
      const c = line[i]
      if (c === '"') { inQ = !inQ }
      else if (c === ',' && !inQ) { result.push(cur); cur = '' }
      else cur += c
    }
    result.push(cur)
    return result
  }

  const rows = lines.map(parseLine)
  const today = new Date().toISOString().split('T')[0]

  const YEAR_BLOCKS = [
    [17, 18, 19], [23, 24, 25], [29, 30, 31], [35, 36, 37], [41, 42, 43]
  ]

  const valid: Record<string, unknown>[] = []
  const review: Record<string, unknown>[] = []

  for (let ri = 2; ri < rows.length; ri++) {
    const row = rows[ri]
    const client_name = getCol(row, 3)
    if (!client_name || client_name === 'キャンセル') continue

    const mgmt_no      = getCol(row, 2)
    const product_type = getCol(row, 7)
    const serial_hard  = getCol(row, 8)
    const serial_bill  = getCol(row, 9)
    const notes_raw    = getCol(row, 47)

    let best: Record<string, unknown> | null = null

    // 最新年（データが入っている最後の年）を使う → 逆順ループで最初に見つかったものを採用
    for (const [si, ei, ni] of [...YEAR_BLOCKS].reverse()) {
      const s = parseDate(getCol(row, si))
      const e = parseDate(getCol(row, ei))
      const plan = getCol(row, ni)
      if (!e || !plan || plan === '保守無し') continue
      // end_dateが未来 or 過去どちらでもデータがあれば最新年として採用
      best = { start_date: s, end_date: e, plan_name: plan, plan_type: 'paid' }
      break
    }

    if (!best) {
      const s = parseDate(getCol(row, 13))
      const e = parseDate(getCol(row, 14))
      if (e && e >= today) {
        best = { start_date: s, end_date: e, plan_name: '無償保守', plan_type: 'free' }
      }
    }

    const base = { client_name, management_no: mgmt_no, product_type, serial_no_hard: serial_hard, serial_no_bill: serial_bill, notes: notes_raw }

    if (best) {
      valid.push({ ...base, ...best, status: 'active' })
    } else {
      // 最後の終了日を探す
      let lastEnd: string | null = null
      let lastPlan: string | null = null
      for (const [, ei, ni] of YEAR_BLOCKS) {
        const e = parseDate(getCol(row, ei))
        const plan = getCol(row, ni)
        if (e && plan && plan !== '保守無し') { lastEnd = e; lastPlan = plan }
      }
      const freeEnd = parseDate(getCol(row, 14))
      const end_date = lastEnd || freeEnd || '2020-01-01'
      review.push({
        ...base,
        plan_name: lastPlan || '無償保守',
        plan_type: lastPlan ? 'paid' : 'free',
        end_date,
        start_date: null,
        notes: (notes_raw ? notes_raw + ' / ' : '') + '要確認',
        status: 'needs_review',
      })
    }
  }

  // 既存データを全削除してインポート（upsert）
  const { error: delErr } = await supabase
    .from('paycube_contracts')
    .delete()
    .neq('id', '00000000-0000-0000-0000-000000000000') // 全削除

  if (delErr) return NextResponse.json({ error: delErr.message }, { status: 500 })

  const all = [...valid, ...review]
  if (all.length > 0) {
    const { error: insErr } = await supabase
      .from('paycube_contracts')
      .insert(all)
    if (insErr) return NextResponse.json({ error: insErr.message }, { status: 500 })
  }

  return NextResponse.json({
    ok: true,
    imported: valid.length,
    needs_review: review.length,
    total: all.length,
    timestamp: new Date().toISOString(),
  })
}
