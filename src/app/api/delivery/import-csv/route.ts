import { createClient } from '@supabase/supabase-js'
import { NextRequest, NextResponse } from 'next/server'
import crypto from 'crypto'

export const runtime = 'nodejs'

function parseDate(s: string): string | null {
  if (!s) return null
  s = s.trim()
  if (!s || s === '--' || s === '-') return null
  const m = s.match(/^(\d{4})[\/-](\d{1,2})[\/-](\d{1,2})/)
  if (m) return `${m[1]}-${String(m[2]).padStart(2, '0')}-${String(m[3]).padStart(2, '0')}`
  return null
}

function getCol(row: string[], idx: number): string {
  return (row[idx] || '').trim()
}

// CSVパース（簡易・ダブルクォート対応・CRLF/LF両対応）
function parseCSV(text: string): string[][] {
  const rows: string[][] = []
  let row: string[] = []
  let cur = ''
  let inQ = false
  for (let i = 0; i < text.length; i++) {
    const c = text[i]
    if (inQ) {
      if (c === '"') {
        if (text[i + 1] === '"') { cur += '"'; i++ }
        else inQ = false
      } else cur += c
    } else {
      if (c === '"') inQ = true
      else if (c === ',') { row.push(cur); cur = '' }
      else if (c === '\n') { row.push(cur); rows.push(row); row = []; cur = '' }
      else if (c === '\r') { /* skip */ }
      else cur += c
    }
  }
  if (cur !== '' || row.length > 0) { row.push(cur); rows.push(row) }
  return rows
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
  const rows = parseCSV(text)

  // ヘッダー行(0行目)をスキップしてデータ行から取り込み
  // 列: 0=連番,1=企業名,2=設置先住所,3=製品名,4=台数,5=進捗,6=担当,7=納品予定日,8=納品日,
  //     ...,29=担当者名,30=担当連絡先①,31=担当連絡先②,32=備考
  const items: Record<string, unknown>[] = []
  for (let ri = 1; ri < rows.length; ri++) {
    const row = rows[ri]
    const client_name = getCol(row, 1)
    if (!client_name) continue

    const install_address = getCol(row, 2)
    const product_name = getCol(row, 3)
    const quantityRaw = getCol(row, 4)
    const quantity = quantityRaw ? parseInt(quantityRaw, 10) : null
    const progress = getCol(row, 5)
    const assignee = getCol(row, 6)
    const delivery_due_date = parseDate(getCol(row, 7))
    const delivery_date = parseDate(getCol(row, 8))
    const contact_name = getCol(row, 29)
    const contact_tel1 = getCol(row, 30)
    const contact_tel2 = getCol(row, 31)
    const notes = getCol(row, 32)

    if (!delivery_due_date) continue // 納品予定日がない行はスキップ

    const status = delivery_date ? 'done' : 'active'

    const hashSrc = `${client_name}|${install_address}|${product_name}|${delivery_due_date}`
    const row_hash = crypto.createHash('md5').update(hashSrc).digest('hex')

    items.push({
      client_name, install_address, product_name,
      quantity: Number.isFinite(quantity) ? quantity : null,
      progress, assignee,
      delivery_due_date, delivery_date,
      contact_name, contact_tel1, contact_tel2, notes,
      status, row_hash,
    })
  }

  // 既存データを全削除してインポート（PayCubeと同じ方式：常に最新スナップショットに置き換え）
  const { error: delErr } = await supabase
    .from('delivery_items')
    .delete()
    .neq('id', '00000000-0000-0000-0000-000000000000')

  if (delErr) return NextResponse.json({ error: delErr.message }, { status: 500 })

  if (items.length > 0) {
    const { error: insErr } = await supabase
      .from('delivery_items')
      .insert(items)
    if (insErr) return NextResponse.json({ error: insErr.message }, { status: 500 })
  }

  return NextResponse.json({
    ok: true,
    imported: items.length,
    timestamp: new Date().toISOString(),
  })
}
