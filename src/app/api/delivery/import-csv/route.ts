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
  //     9=KTS登録,10=訪問日,
  //     11=PMS,12=カードディスペンサー,13=カードキー種類,14=キーボックス,15=スマートロック,
  //     16=PayCube,17=VEGA3000,18=P400,19=パスポートリーダー,
  //     20=Surface用スタンド,21=Surface用タッチペン,22=Surface用発券用プリンター,23=Surface用カードロックライター,
  //     24=卓上QRコードリーダー,25=雨除けカバー,26=タブレットスタンド（鍵付）,27=タブレットスタンド,
  //     28=請求書発行,29=担当者名,30=担当連絡先①,31=担当連絡先②,32=備考,33=備考,
  //     34=VEGA3000手配状況,35=P400手配状況,36=PayCube手配状況
  const EQUIPMENT_COLS: { idx: number; name: string }[] = [
    { idx: 11, name: 'PMS' },
    { idx: 12, name: 'カードディスペンサー' },
    { idx: 13, name: 'カードキー種類' },
    { idx: 14, name: 'キーボックス' },
    { idx: 15, name: 'スマートロック' },
    { idx: 16, name: 'PayCube' },
    { idx: 17, name: 'VEGA3000' },
    { idx: 18, name: 'P400' },
    { idx: 19, name: 'パスポートリーダー' },
    { idx: 20, name: 'Surface用スタンド' },
    { idx: 21, name: 'Surface用タッチペン' },
    { idx: 22, name: 'Surface用発券用プリンター' },
    { idx: 23, name: 'Surface用カードロックライター' },
    { idx: 24, name: '卓上QRコードリーダー' },
    { idx: 25, name: '雨除けカバー' },
    { idx: 26, name: 'タブレットスタンド（鍵付）' },
    { idx: 27, name: 'タブレットスタンド' },
  ]

  function isEmptyEquipmentValue(v: string): boolean {
    return !v || v === '--' || v === '-'
  }

  // 既存の delivery_items から item_key→status を取得しておく。
  // ダッシュボードで手動「納品完了」にした案件は、CSV側の納品日が空欄のままでも
  // CSV再取込で「active」に巻き戻らないようにするため。
  const { data: existingRows } = await supabase
    .from('delivery_items')
    .select('item_key, status, dashboard_todos')
  const existingStatusMap = new Map<string, string>()
  // [MANUAL_DUEDATE_V1 2026-10-29] ダッシュボードで手動変更した納品予定日。
  //   画面(L1753付近)で納期を直せるのに、従来はCSV値で毎回上書きされ巻き戻っていた。
  //   手動値は dashboard_todos.manual_due_date にあり import は触らないので、
  //   ここで読み出して「手動値があればCSVより優先」する。
  const manualDueMap = new Map<string, string>()
  for (const row of existingRows || []) {
    existingStatusMap.set(row.item_key, row.status)
    const md = (row.dashboard_todos || {})['manual_due_date']
    if (md) manualDueMap.set(row.item_key, String(md))
  }

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
    const notes = [getCol(row, 32), getCol(row, 33)].filter(Boolean).join(' / ')

    // 長納期機器の手配状況（例：発注済み/未発注/納品済み 等が入っている想定）
    // [MANUAL_EQUIP_STATUS_V1 2026-10-29] これらは「CSV由来の列」。毎回上書きされる。
    //   ダッシュボードで手動設定した値は p400_status_manual 等の専用列に入っており、
    //   ここでは一切触らないので再取込しても保持される。
    //   ⚠ UIから *_status(CSV列)へ手動値を書き込まないこと(再取込で必ず消える)。
    const vega3000_status = getCol(row, 34)
    const p400_status = getCol(row, 35)
    const paycube_status = getCol(row, 36)
    // 進行中シートにある追加列（37=P400 MTID, 38=P400 TID）
    const p400_mtid = getCol(row, 37) || null
    const p400_tid  = getCol(row, 38) || null

    // 「--」でない機器列だけを抽出し、どの機器が必要な案件かを保存する
    const equipment = EQUIPMENT_COLS
      .map(c => ({ name: c.name, value: getCol(row, c.idx) }))
      .filter(e => !isEmptyEquipmentValue(e.value))

    if (!delivery_due_date) continue // 納品予定日がない行はスキップ

    // item_key: 会社名＋設置先住所＋製品名から生成する「案件の身元」。
    // 納期や進捗が変わってもこのキーは変わらないので、ダッシュボード側の手動入力
    // （manual_ordered / dashboard_memo / checked_by 等）を同じ行に紐づけ続けられる。
    const item_key = crypto.createHash('md5')
      .update(`${client_name}|${install_address}|${product_name}`)
      .digest('hex')

    // CSVの納品日が入っていれば done。
    // 入っていなくても、ダッシュボードで既に手動 done 化されている場合はそのまま done を維持する
    // （「納品完了にする」を押した案件が、CSVの納品日未入力のせいでまた復活するのを防ぐ）。
    const status = delivery_date
      ? 'done'
      : (existingStatusMap.get(item_key) === 'done' ? 'done' : 'active')

    // [MANUAL_DUEDATE_V1] 手動で直した納期があればそちらを採用(CSVより優先)
    const manualDue = manualDueMap.get(item_key)
    const final_due_date = manualDue || delivery_due_date

    const hashSrc = `${client_name}|${install_address}|${product_name}|${delivery_due_date}`
    const row_hash = crypto.createHash('md5').update(hashSrc).digest('hex')

    items.push({
      item_key,
      client_name, install_address, product_name,
      quantity: Number.isFinite(quantity) ? quantity : null,
      progress, assignee,
      delivery_due_date: final_due_date, delivery_date,   // [MANUAL_DUEDATE_V1] 手動値優先
      contact_name, contact_tel1, contact_tel2, notes,
      status, row_hash,
      equipment,
      vega3000_status, p400_status, paycube_status,
      ...(p400_mtid ? { p400_mtid } : {}),
      ...(p400_tid  ? { p400_tid  } : {}),
      missing_in_last_import: false,
      last_imported_at: new Date().toISOString(),
    })
  }

  // 既存の全行をいったん「今回のCSVに存在しない」フラグON状態にしておき、
  // upsert後に今回のCSVに含まれる行だけ missing_in_last_import=false に戻る。
  // → ダッシュボード側の手動入力（manual_ordered等）は一切触らずに保持される。
  const { error: markErr } = await supabase
    .from('delivery_items')
    .update({ missing_in_last_import: true })
    .neq('id', '00000000-0000-0000-0000-000000000000')
  if (markErr) return NextResponse.json({ error: markErr.message }, { status: 500 })

  // 同じCSV内で item_key（会社名＋住所＋製品名）が重複する行がある場合、
  // upsertが「同一トランザクション内で同じ行を2回更新」してエラーになるため、
  // 後に出てきた行を優先して1件にまとめる（同じ案件の台数・進捗が複数行に分かれているケースを統合）。
  const dedupedMap = new Map<string, Record<string, unknown>>()
  for (const item of items) {
    dedupedMap.set(item.item_key as string, item)
  }
  const dedupedItems = Array.from(dedupedMap.values())

  if (dedupedItems.length > 0) {
    // item_key で upsert：既存行はCSV由来の列だけ上書きされ、
    // manual_ordered / dashboard_memo / checked_by / checked_at は対象外なので保持される。
    const { error: upErr } = await supabase
      .from('delivery_items')
      .upsert(dedupedItems, { onConflict: 'item_key' })
    if (upErr) return NextResponse.json({ error: upErr.message }, { status: 500 })
  }

  return NextResponse.json({
    ok: true,
    imported: dedupedItems.length,
    timestamp: new Date().toISOString(),
  })
}
