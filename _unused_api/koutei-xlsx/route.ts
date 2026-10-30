// [KOUTEI_XLSX_V1 2026-10-29]
// 工程管理表の原本から、その案件に不要な行（使わない機材の工程）を削ったExcelを生成する。
// ヒアリングシートと同じ方式。Googleドライブにアップすればスプレッドシートになる。
import { NextRequest, NextResponse } from 'next/server'
import ExcelJS from 'exceljs'
import { KOUTEI_ROWS, KOUTEI_CATEGORY_KEYS } from '@/lib/kouteiDef'

export const runtime = 'nodejs'

type Body = {
  flags?: Record<string, boolean>   // 例 { pms:true, smartlock:true, p400:false ... }
  info?: Record<string, string>     // 会社名/物件名/稼働予定日
}

export async function POST(req: NextRequest) {
  let body: Body
  try {
    body = await req.json()
  } catch {
    return NextResponse.json({ error: 'invalid json' }, { status: 400 })
  }
  const flags = body.flags || {}
  const info = body.info || {}

  const wb = new ExcelJS.Workbook()
  wb.creator = 'KUJIRA Support'
  wb.created = new Date()
  const ws = wb.addWorksheet('工程管理')

  // 原本の列構成に合わせる
  ws.columns = [
    { width: 6 },   // A No
    { width: 12 },  // B 品目
    { width: 22 },  // C 区分
    { width: 26 },  // D 作業名
    { width: 26 },  // E 対応に要する期間
    { width: 54 },  // F 詳細
    { width: 12 },  // G 担当部署
    { width: 10 },  // H 担当者
    { width: 12 },  // I ステータス
    { width: 14 },  // J 完了予定日
    { width: 12 },  // K 完了日
    { width: 10 },  // L 進捗
    { width: 54 },  // M 備考
    { width: 8 },   // N
    { width: 8 },   // O
  ]

  let kept = 0
  let removed = 0

  KOUTEI_ROWS.forEach((row, ri) => {
    // 先頭3行（ヘッダ・列見出し）は常に残す
    if (ri < 3) {
      const vals = [...row]
      // 会社名・物件名・稼働予定日を差し込む
      if (ri === 0) {
        if (info.client) vals[1] = info.client
        if (info.due) vals[6] = info.due
      }
      if (ri === 1 && info.property) vals[1] = info.property
      const r = ws.addRow(vals)
      r.alignment = { wrapText: true, vertical: 'middle' }
      if (ri === 2) {
        r.font = { bold: true }
        r.eachCell({ includeEmpty: false }, c => {
          c.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFDCE6F1' } }
          c.border = {
            top: { style: 'thin' }, bottom: { style: 'thin' },
            left: { style: 'thin' }, right: { style: 'thin' },
          }
        })
      }
      return
    }

    // C列(index 2)の区分で要否を判定
    const cat = (row[2] || '').trim()
    if (cat) {
      const key = KOUTEI_CATEGORY_KEYS[cat]
      if (key && key !== 'always' && !flags[key]) {
        removed++
        return   // この機材は使わないので行ごと削除
      }
    }

    const r = ws.addRow(row)
    r.alignment = { wrapText: true, vertical: 'top' }
    kept++

    // 品目で色分け（事前準備/現地訪問/設置後対応）
    const item = (row[1] || '').trim()
    const bg = item === '現地訪問' ? 'FFFFF2CC'
      : item === '設置後対応' ? 'FFE2EFDA'
      : null
    if (bg) {
      r.getCell(2).fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: bg } }
    }
    // 行高（詳細が長いので折り返しを潰さない）
    const longest = Math.max(...row.map(v => (v || '').length), 0)
    if (longest > 50) r.height = Math.min(80, 15 + Math.ceil(longest / 50) * 13)
  })

  ws.views = [{ state: 'frozen', xSplit: 0, ySplit: 3 }]
  ws.autoFilter = { from: { row: 3, column: 1 }, to: { row: 3, column: 13 } }

  const buf = await wb.xlsx.writeBuffer()
  const fname = `工程管理_${(info.client || '').replace(/[\\/:*?"<>|]/g, '')}_${new Date().toISOString().slice(0, 10)}.xlsx`
  return new NextResponse(buf as ArrayBuffer, {
    status: 200,
    headers: {
      'Content-Type': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
      'Content-Disposition': `attachment; filename*=UTF-8''${encodeURIComponent(fname)}`,
      'X-Rows-Kept': String(kept),
      'X-Rows-Removed': String(removed),
    },
  })
}
