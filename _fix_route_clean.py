# -*- coding: utf-8 -*-
"""[HEARING_XLSX_V5 2026-10-29] マージ処理を1本化して、雛形と同じ見た目にする。

これまでの問題:
  ・雛形は A1:K1 等を結合しているが、CSV化で結合情報が消え全セルに同じ文字列が入る
  ・それをそのまま出力したので1行に同じ文章が11個並んだ
  ・修正を重ねた結果、マージ処理が2系統(V3とV4)混在して競合していた

対策: シート描画部を作り直し、マージ処理を1箇所に統一する。
  1. 行内で連続する同一文字列 -> 先頭のみ残して結合（雛形の結合を復元）
  2. 回答欄(□)は L列固定で黄色+罫線
  3. 見出し/説明文/設問でスタイルを分ける
"""
import io, shutil, datetime, re

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\hearing-xlsx\route.ts"
bak = P + ".bak_v5_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
src = io.open(P, encoding="utf-8").read()

# 「for (const name of sheets) {」から、その直前の「const buf =」までを差し替える
i = src.index("  for (const name of sheets) {")
j = src.index("  const buf = await wb.xlsx.writeBuffer()")

NEW = '''  for (const name of sheets) {
    const def = HEARING_SHEET_DEFS[name]
    const ws = wb.addWorksheet(name.slice(0, 31))
    if (!def || !def.length) {
      ws.addRow([`【${name}】の定義が未登録です`])
      ws.addRow(['雛形スプレッドシートの該当シートを転記してください。'])
      continue
    }

    // [HEARING_XLSX_V5 2026-10-29] 列幅。雛形の列位置を保持した定義を前提にする。
    //   A列=大見出し/説明文, B列=設問, D列=設問(2段目), L列=ご回答欄
    const ANS = 12                                   // L列 = 回答欄
    const maxCols = Math.max(...def.map(r => r.length), ANS)
    ws.columns = Array.from({ length: maxCols }, (_, i) => {
      if (i === 0) return { width: 4 }
      if (i === 1) return { width: 8 }
      if (i === 2) return { width: 4 }
      if (i === 3) return { width: 8 }
      if (i === ANS - 1) return { width: 26 }        // ご回答欄
      if (i >= ANS) return { width: 44 }             // 備考など
      return { width: 8 }
    })

    const merges: Array<[number, number, number]> = []

    def.forEach((row, ri) => {
      const vals = row.map(c => {
        const hit = Object.keys(prefill).find(k => c.includes(k))
        if (c === '□' && hit) return prefill[hit] === 'TRUE' ? '✔' : '□'
        return c
      })

      // --- 雛形の結合を復元する ---
      //   CSV化で失われた結合は「同じ文字列が連続する」形で残っているので、
      //   連続区間を1セルに畳んで結合する。
      let c = 0
      while (c < vals.length) {
        const v = vals[c]
        if (v) {
          let e = c
          while (e + 1 < vals.length && vals[e + 1] === v) e++
          if (e > c) {
            for (let k = c + 1; k <= e; k++) vals[k] = ''
            merges.push([ri + 1, c + 1, e + 1])
          }
          c = e + 1
        } else {
          c++
        }
      }

      const r = ws.addRow(vals)
      r.alignment = { wrapText: true, vertical: 'middle' }

      r.eachCell({ includeEmpty: false }, (cell, col) => {
        const v = String(cell.value ?? '')
        if (!v) return
        if (v === '□' || v === '✔') {
          cell.fill = YELLOW
          cell.alignment = { horizontal: 'center', vertical: 'middle' }
          cell.border = {
            top: { style: 'thin' }, bottom: { style: 'thin' },
            left: { style: 'thin' }, right: { style: 'thin' },
          }
          cell.font = { size: 12, bold: true }
          return
        }
        if (ri === 0) {                               // シート見出し
          cell.font = { bold: true, size: 13 }
          return
        }
        if (/^\\s*\\d+\\.\\s/.test(v)) {                 // 1. 2. の大見出し
          cell.font = { bold: true, size: 11 }
          cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFDCE6F1' } }
          return
        }
        if (v.startsWith('※') || v.startsWith('・') || v.startsWith('AdvaNceD')) {
          cell.font = { size: 9, color: { argb: 'FF666666' } }   // 説明文
          return
        }
        if (col >= ANS + 1) {
          cell.font = { size: 9, color: { argb: 'FF666666' } }   // 備考列
        }
      })

      // 行高は内容量から推定（折り返しが潰れないように）
      const longest = Math.max(...vals.map(v => (v || '').length), 0)
      if (longest > 60) r.height = Math.min(90, 16 + Math.ceil(longest / 60) * 14)
    })

    for (const [row, c1, c2] of merges) {
      try { ws.mergeCells(row, c1, row, c2) } catch { /* 既に結合済みなら無視 */ }
    }
    ws.views = [{ state: 'frozen', ySplit: 1 }]
  }

'''
src = src[:i] + NEW + src[j:]
io.open(P, "w", encoding="utf-8").write(src)
print("rewritten")
