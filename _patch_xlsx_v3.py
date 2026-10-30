# -*- coding: utf-8 -*-
"""[HEARING_XLSX_V3 2026-10-29] Excelの見た目を雛形スプレッドシートに合わせる。

ユーザー指摘「全然スプシと違う」。雛形の実構造を確認した結果:
  A列 = 大見出し(1. 物件で利用する『鍵』について) / 説明文
  B列 = 設問(1段目)
  D列 = 設問(2段目。決済手段の4項目)
  L列 = ご回答欄

対策:
 ・列幅を実データから算出（決め打ちをやめる）
 ・A〜K列は設問テキストが跨って読めるよう、設問行は横方向に結合
 ・見出し行/説明行/設問行を見分けて書式を変える
 ・行の高さを内容に応じて確保
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\hearing-xlsx\route.ts"
bak = P + ".bak_v3_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

i = s.index("  for (const name of sheets) {")
j = s.index("  const buf = await wb.xlsx.writeBuffer()")

NEW = '''  for (const name of sheets) {
    const def = HEARING_SHEET_DEFS[name]
    const ws = wb.addWorksheet(name.slice(0, 31))
    if (!def || !def.length) {
      ws.addRow([`【${name}】の定義が未登録です`])
      ws.addRow(['雛形スプレッドシートの該当シートを転記してください。'])
      continue
    }

    // [HEARING_XLSX_V3] 雛形の構造を再現する。
    //   A列=大見出し/説明文, B列=設問, D列=設問(2段目), L列=ご回答欄
    const maxCols = Math.max(...def.map(r => r.length), 12)
    const ANS = 11                      // L列(0始まり)
    ws.columns = Array.from({ length: maxCols }, (_, i) => {
      if (i === 0) return { width: 4 }    // A列はインデント用に細く
      if (i === 1) return { width: 4 }
      if (i === ANS) return { width: 24 } // ご回答欄
      if (i > ANS) return { width: 30 }   // 備考
      return { width: 4 }
    })

    def.forEach((row, ri) => {
      const vals = row.map(c => {
        const hit = Object.keys(prefill).find(k => c.includes(k))
        if (c === '□' && hit) return prefill[hit] === 'TRUE' ? '✔' : '□'
        return c
      })
      const r = ws.addRow(vals)
      r.alignment = { wrapText: true, vertical: 'middle' }

      // テキストが入っている最初の列を調べ、A〜K列を結合して読めるようにする
      let firstText = -1
      for (let c = 0; c < Math.min(vals.length, ANS); c++) {
        if (vals[c] && vals[c] !== '□') { firstText = c; break }
      }
      if (firstText >= 0) {
        try { ws.mergeCells(r.number, firstText + 1, r.number, ANS) } catch { /* 既に結合済み */ }
        const cell = r.getCell(firstText + 1)
        cell.alignment = { wrapText: true, vertical: 'middle' }
        const v = String(vals[firstText])
        if (ri === 0) {
          cell.font = { bold: true, size: 13 }
        } else if (/^\\s*\\d+\\.\\s/.test(v)) {
          // 大見出し
          cell.font = { bold: true, size: 11 }
          cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFDCE6F1' } }
        } else if (v.startsWith('※') || v.startsWith('・') || v.startsWith('AdvaNceD')) {
          // 説明文
          cell.font = { size: 9, color: { argb: 'FF555555' } }
        }
        // 行の高さを文字数から推定
        const len = v.length
        r.height = Math.min(120, Math.max(20, Math.ceil(len / 60) * 16 + 6))
      }

      // 回答欄
      r.eachCell({ includeEmpty: false }, (cell) => {
        const v = String(cell.value ?? '')
        if (v === '□' || v === '✔') {
          cell.fill = YELLOW
          cell.alignment = { horizontal: 'center', vertical: 'middle' }
          cell.font = { bold: true, size: 12 }
          cell.border = {
            top: { style: 'thin' }, bottom: { style: 'thin' },
            left: { style: 'thin' }, right: { style: 'thin' },
          }
        }
      })
    })
    ws.views = [{ state: 'frozen', ySplit: 1 }]
  }

'''
s = s[:i] + NEW + s[j:]
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
