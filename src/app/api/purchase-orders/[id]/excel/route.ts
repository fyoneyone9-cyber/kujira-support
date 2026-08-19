import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'
import ExcelJS from 'exceljs'

export async function GET(_req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const supabase = await createClient()

  const { data, error } = await supabase
    .from('purchase_orders')
    .select('*, purchase_order_items(*)')
    .eq('id', id)
    .single()

  if (error) return NextResponse.json({ error: error.message }, { status: 404 })

  const order = data
  const items = (order.purchase_order_items || []).sort(
    (a: { sort_order: number }, b: { sort_order: number }) => a.sort_order - b.sort_order
  )

  const workbook = new ExcelJS.Workbook()
  const sheet = workbook.addWorksheet('発注書')

  // 列幅設定
  sheet.getColumn('A').width = 3
  sheet.getColumn('B').width = 30
  sheet.getColumn('C').width = 10
  sheet.getColumn('D').width = 8
  sheet.getColumn('E').width = 12
  sheet.getColumn('F').width = 15
  sheet.getColumn('G').width = 18
  sheet.getColumn('H').width = 18

  // ヘッダー情報
  sheet.getCell('G1').value = 'No.'
  sheet.getCell('H1').value = order.order_no
  sheet.getCell('G2').value = '日付'
  sheet.getCell('H2').value = order.order_date

  // タイトル
  sheet.getCell('B3').value = '発　注　書'
  sheet.getCell('B3').font = { bold: true, size: 18 }

  // 宛先
  sheet.getCell('B4').value = order.vendor_name
  sheet.getCell('E4').value = '御中'
  sheet.getCell('B5').value = order.vendor_zip
  sheet.getCell('B6').value = order.vendor_address
  sheet.getCell('B7').value = order.vendor_tel
  sheet.getCell('B8').value = '下記の通り、ご発注申し上げます。'

  // 条件
  sheet.getCell('B9').value = '支払条件/PAYMENT'
  sheet.getCell('C9').value = order.payment_terms
  sheet.getCell('F9').value = '株式会社デバイスエージェンシー'
  sheet.getCell('F10').value = '〒550-0015'
  sheet.getCell('B11').value = '入荷場所/PLACE OF RECEIPT'
  sheet.getCell('C11').value = order.delivery_place
  sheet.getCell('F11').value = '大阪府大阪市西区靭本町4-17-18'
  sheet.getCell('F12').value = '靭ビルディング1階'
  sheet.getCell('B13').value = '納期/DELIVERY TERMS'
  sheet.getCell('C13').value = order.delivery_date
  sheet.getCell('F13').value = 'TEL：06-6585-9865'
  sheet.getCell('F14').value = 'FAX：06-6585-9875'

  // 合計予定
  sheet.getCell('B15').value = '合計予定'
  sheet.getCell('C15').value = order.total
  sheet.getCell('E15').value = '(税込)'

  // 品目ヘッダー
  const headerRow = sheet.getRow(16)
  headerRow.getCell('B').value = '品　名/DESCRIPTION'
  headerRow.getCell('E').value = '数量/QUANTITY'
  headerRow.getCell('F').value = '単位/UNIT'
  headerRow.getCell('G').value = '単価/UNIT-PRICE'
  headerRow.getCell('H').value = '合計金額/AMOUNT'
  headerRow.font = { bold: true }

  // 品目
  let rowNum = 17
  for (const item of items) {
    const row = sheet.getRow(rowNum)
    row.getCell('B').value = item.description + (item.sub_description ? `\n${item.sub_description}` : '')
    row.getCell('E').value = item.quantity
    row.getCell('F').value = item.unit
    row.getCell('G').value = item.unit_price
    row.getCell('H').value = item.amount
    rowNum++
  }

  // 小計・税・合計
  sheet.getRow(rowNum).getCell('G').value = '小計'
  sheet.getRow(rowNum).getCell('H').value = order.subtotal
  rowNum++
  sheet.getRow(rowNum).getCell('G').value = '消費税(10%)'
  sheet.getRow(rowNum).getCell('H').value = order.tax
  rowNum++
  sheet.getRow(rowNum).getCell('G').value = '合計(税込)'
  sheet.getRow(rowNum).getCell('H').value = order.total
  sheet.getRow(rowNum).font = { bold: true }

  const buffer = await workbook.xlsx.writeBuffer()
  const filename = encodeURIComponent(`発注書_${order.order_no}.xlsx`)

  return new NextResponse(buffer as ArrayBuffer, {
    headers: {
      'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'Content-Disposition': `attachment; filename*=UTF-8''${filename}`,
    },
  })
}
