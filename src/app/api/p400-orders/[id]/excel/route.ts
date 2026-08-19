import { createClient } from '@/lib/supabase/server'
import { NextResponse } from 'next/server'
import ExcelJS from 'exceljs'

export async function GET(_req: Request, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const supabase = await createClient()
  const { data: order, error } = await supabase.from('p400_orders').select('*').eq('id', id).single()
  if (error || !order) return NextResponse.json({ error: 'Not found' }, { status: 404 })

  const workbook = new ExcelJS.Workbook()
  const sheet = workbook.addWorksheet('注文書')

  // Set column widths
  sheet.getColumn('A').width = 12
  sheet.getColumn('B').width = 20
  sheet.getColumn('C').width = 10
  sheet.getColumn('D').width = 10
  sheet.getColumn('E').width = 12
  sheet.getColumn('S').width = 14
  sheet.getColumn('T').width = 20

  // Row 1: order number
  sheet.getCell('S1').value = '注文番号：'
  sheet.getCell('T1').value = order.order_no

  // Row 2: title
  sheet.getCell('A2').value = '注文書'
  sheet.getCell('A2').font = { bold: true, size: 18 }

  // Row 3: addressee
  sheet.getCell('A3').value = 'SBペイメントサービス株式会社'
  sheet.getCell('J3').value = '御中'
  // Right side company info
  sheet.getCell('L3').value = '株式会社デバイスエージェンシー'
  sheet.getCell('L4').value = '〒243-0424 神奈川県海老名市社家6-5-2-301'
  sheet.getCell('L5').value = 'TEL: 080-3207-8422'
  sheet.getCell('L6').value = `担当者: ${order.store_manager || ''}`

  // Row 4: store name
  sheet.getCell('A4').value = `対象店舗：${order.store_name}`

  // Row 5: store address/tel
  if (order.store_address) sheet.getCell('A5').value = `住所：${order.store_address}`
  if (order.store_tel) sheet.getCell('A6').value = `TEL：${order.store_tel}`
  if (order.general_manager) sheet.getCell('A7').value = `総括担当者：${order.general_manager}`

  // Row 8: subject
  sheet.getCell('A8').value = 'Verifone P400の端末機およびセットアップ用に関して、以下のとおり注文申し上げます。'

  // Row 9: total amounts
  sheet.getCell('A9').value = `合計予定金額：${order.total.toLocaleString()}円`
  sheet.getCell('F9').value = `消費税(10%)：${order.tax.toLocaleString()}円`

  // Row 10: delivery info
  sheet.getCell('A10').value = `入荷場所：${order.delivery_place || ''}`
  sheet.getCell('F10').value = '受領：別途請求'
  sheet.getCell('K10').value = `支払条件：${order.payment_terms || '別途請求'}`

  // Row 12: table header
  const headerRow = sheet.getRow(12)
  headerRow.values = ['', '番号', '品名', '', '', '数量', '単価(税抜)', '合計']
  headerRow.font = { bold: true }
  headerRow.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFD9D9D9' } }

  const items = [
    { name: 'Verifone P400', qty: order.qty_p400, price: 49800 },
    { name: 'セットアップ用（クレジット・電子マネー）', qty: order.qty_setup_credit, price: 6000 },
    { name: 'セットアップ用（電子マネー）', qty: order.qty_setup_emoney, price: 10000 },
    { name: 'セットアップ用（QRコード）', qty: order.qty_setup_qr, price: 6000 },
    { name: 'RS-232Cケーブル(1m)', qty: order.qty_cable, price: 4800 },
  ]

  let rowIdx = 13
  let itemNo = 1
  for (const item of items) {
    if (item.qty > 0) {
      const row = sheet.getRow(rowIdx)
      row.values = ['', itemNo, item.name, '', '', item.qty, item.price, item.qty * item.price]
      rowIdx++
      itemNo++
    }
  }

  // Subtotal / tax / total
  sheet.getRow(rowIdx).values = ['', '', '', '', '', '', '小計', order.subtotal]
  rowIdx++
  sheet.getRow(rowIdx).values = ['', '', '', '', '', '', '消費税(10%)', order.tax]
  rowIdx++
  const totalRow = sheet.getRow(rowIdx)
  totalRow.values = ['', '', '', '', '', '', '合計(税込)', order.total]
  totalRow.font = { bold: true }
  rowIdx += 2

  // Notes
  const notesText = [
    order.notes,
    '基本加盟店証明書番号：2023年11月22日付「加盟店証明書」',
    '信販会社管理番号：SBPS-20231027DA',
  ].filter(Boolean).join('\n')
  sheet.getCell(`A${rowIdx}`).value = '備考：'
  sheet.getCell(`B${rowIdx}`).value = notesText
  sheet.getCell(`B${rowIdx}`).alignment = { wrapText: true }

  const buffer = await workbook.xlsx.writeBuffer()
  const filename = encodeURIComponent(`P400注文書_${order.order_no}.xlsx`)

  return new NextResponse(buffer, {
    headers: {
      'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'Content-Disposition': `attachment; filename*=UTF-8''${filename}`,
    },
  })
}
