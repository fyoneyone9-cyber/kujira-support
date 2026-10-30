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
function toInt(s: string): number {
  const n = parseInt((s || '').replace(/[^0-9\-]/g, ''), 10)
  return isNaN(n) ? 0 : n
}
function parseCSV(text: string): string[][] {
  const rows: string[][] = []
  let row: string[] = []; let cur = ''; let inQ = false
  for (let i = 0; i < text.length; i++) {
    const c = text[i]
    if (inQ) {
      if (c === '"') { if (text[i + 1] === '"') { cur += '"'; i++ } else inQ = false }
      else cur += c
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
  if (rows.length < 2) return NextResponse.json({ error: 'データが不足しています' }, { status: 400 })

  // 1行目: 最終棚卸日メタ（例: 最終棚卸日：,2026/06/01,...）
  let stocktakeDate: string | null = null
  const first = rows[0]
  if (first && /棚卸/.test(first[0] || '')) stocktakeDate = parseDate(first[1] || '')

  // ヘッダ行を探す（品番/製品名/在庫 を含む行）
  let headerIdx = rows.findIndex(r => (r[0] || '').includes('品番') || (r[1] || '').includes('製品名'))
  if (headerIdx < 0) headerIdx = 1
  const header = rows[headerIdx].map(h => (h || '').trim())
  const col = (name: string) => header.findIndex(h => h.replace(/\s/g, '').includes(name))
  const ci = {
    part: col('品番'), name: col('製品名'), stock: col('在庫'),
    incoming: col('入荷予定'), required: col('必要数'), diff: col('差分'), notes: col('備考'),
  }
  const nameIdx = ci.name >= 0 ? ci.name : 1

  const importedAt = new Date().toISOString()
  const seenNames = new Set<string>()
  const records: Record<string, unknown>[] = []
  for (let r = headerIdx + 1; r < rows.length; r++) {
    const row = rows[r]
    const pname = (row[nameIdx] || '').trim()
    if (!pname) continue
    seenNames.add(pname)
    const rowHash = crypto.createHash('md5').update(row.join('|')).digest('hex')
    records.push({
      part_no: ci.part >= 0 ? (row[ci.part] || '').trim() : null,
      product_name: pname,
      stock: ci.stock >= 0 ? toInt(row[ci.stock]) : 0,
      incoming: ci.incoming >= 0 ? toInt(row[ci.incoming]) : 0,
      required: ci.required >= 0 ? toInt(row[ci.required]) : 0,
      diff: ci.diff >= 0 ? toInt(row[ci.diff]) : 0,
      notes: ci.notes >= 0 ? (row[ci.notes] || '').trim() : null,
      last_stocktake_date: stocktakeDate,
      row_hash: rowHash,
      missing_in_last_import: false,
      imported_at: importedAt,
      updated_at: importedAt,
    })
  }
  if (records.length === 0) return NextResponse.json({ error: '取込対象の行がありません' }, { status: 400 })

  // 既存取得（製品名キーでupsert判定）
  const { data: existing } = await supabase.from('inventory_items').select('id, product_name')
  const byName = new Map((existing || []).map(e => [e.product_name, e.id]))

  let inserted = 0, updated = 0
  for (const rec of records) {
    const id = byName.get(rec.product_name as string)
    if (id) {
      await supabase.from('inventory_items').update(rec).eq('id', id)
      updated++
    } else {
      await supabase.from('inventory_items').insert(rec)
      inserted++
    }
  }
  // 今回CSVに無かった既存品は missing フラグを立てる
  const missingIds = (existing || []).filter(e => !seenNames.has(e.product_name)).map(e => e.id)
  if (missingIds.length > 0) {
    await supabase.from('inventory_items').update({ missing_in_last_import: true }).in('id', missingIds)
  }

  return NextResponse.json({ ok: true, inserted, updated, missing: missingIds.length, stocktake_date: stocktakeDate })
}
