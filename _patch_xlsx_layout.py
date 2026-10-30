# -*- coding: utf-8 -*-
"""[HEARING_XLSX_V2 2026-10-29] 列位置を保った定義に合わせてExcel生成を直す。

V1の不具合: 定義側が左詰めだったため列幅も決め打ちで、
            見出し(A列)と設問(B列)の階層・回答欄(L列)の位置が崩れていた。
V3定義では雛形どおりの列位置になったので、Excel側も素直にそのまま出す。
 ・A列=見出し, B列=設問(広め), L列=回答欄
 ・結合はせず、雛形と同じセル配置を維持
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\hearing-xlsx\route.ts"
bak = P + ".bak_layout_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """    // 列幅を内容から推定
    const maxCols = Math.max(...def.map(r => r.length))
    ws.columns = Array.from({ length: maxCols }, (_, i) => ({ width: i === 0 ? 8 : (i === 1 ? 64 : 18) }))"""
assert s.count(OLD) == 1, "anchor1"
NEW = """    // [HEARING_XLSX_V2] 定義は雛形の列位置を保持している。
    //   A列=見出し / B列=設問 / L列(index 11)=回答欄 という構造なので、
    //   その並びが読めるように列幅を割り当てる。
    const maxCols = Math.max(...def.map(r => r.length), 12)
    ws.columns = Array.from({ length: maxCols }, (_, i) => {
      if (i === 0) return { width: 34 }   // 見出し（1. 物件で利用する『鍵』について 等）
      if (i === 1) return { width: 76 }   // 設問本文
      if (i === 11) return { width: 22 }  // ご回答欄
      return { width: 3 }                 // 雛形の空き列（レイアウト維持用）
    })"""
s = s.replace(OLD, NEW, 1)

OLD2 = """      const r = ws.addRow(vals)
      r.alignment = { wrapText: true, vertical: 'top' }
      if (ri === 0) r.font = { bold: true, size: 12 }
      // 回答欄（□）は黄色で塗る
      r.eachCell((cell) => {
        if (cell.value === '□') cell.fill = YELLOW
      })"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """      const r = ws.addRow(vals)
      r.alignment = { wrapText: true, vertical: 'top' }
      if (ri === 0) r.font = { bold: true, size: 13 }
      r.eachCell({ includeEmpty: false }, (cell, col) => {
        const v = String(cell.value ?? '')
        // 回答欄（□）は黄色で塗り、枠線を付けて記入箇所を明示
        if (v === '□') {
          cell.fill = YELLOW
          cell.alignment = { horizontal: 'center', vertical: 'middle' }
          cell.border = {
            top: { style: 'thin' }, bottom: { style: 'thin' },
            left: { style: 'thin' }, right: { style: 'thin' },
          }
        }
        // A列の見出し（1. / 2. で始まる）は太字＋薄い背景
        if (col === 1 && /^\\s*\\d+\\./.test(v)) {
          cell.font = { bold: true }
          cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFE8EEF7' } }
        }
      })"""
s = s.replace(OLD2, NEW2, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
