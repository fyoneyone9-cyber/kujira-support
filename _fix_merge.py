# -*- coding: utf-8 -*-
"""[HEARING_XLSX_V3 2026-10-29] 同じ文字がA〜K列に11回複製される問題の修正。

原因: 雛形スプレッドシートは「A1:K1を結合して1つの見出し」という作りだが、
      CSVに書き出すと結合情報が失われ、全セルに同じ文字列が入る。
      それをそのままExcelに流したので、1行に同じ文章が11個並んでいた。

対策:
  ・行内で連続する同一文字列は先頭だけ残し、残りは空にする
  ・そのうえで該当範囲をセル結合して雛形と同じ見た目にする
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\hearing-xlsx\route.ts"
bak = P + ".bak_merge_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """    def.forEach((row, ri) => {
      const vals = row.map(c => {"""
assert s.count(OLD) == 1, "anchor1"
NEW = """    // [HEARING_XLSX_V3 2026-10-29] 雛形は A1:K1 等を結合して1つの見出しにしている。
    //   CSV化すると結合情報が失われ全セルに同じ文字列が複製されるため、
    //   連続する同一文字列は先頭だけ残して結合し直す。
    const merges: [number, number, number][] = []   // [行, 開始列, 終了列]
    def.forEach((row, ri) => {
      const vals = row.map(c => {"""
s = s.replace(OLD, NEW, 1)

OLD2 = """      const r = ws.addRow(vals)"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """      // 連続する同一文字列を畳む（結合対象として記録）
      let i = 0
      while (i < vals.length) {
        const v = vals[i]
        if (v) {
          let j = i
          while (j + 1 < vals.length && vals[j + 1] === v) j++
          if (j > i) {
            for (let k = i + 1; k <= j; k++) vals[k] = ''
            merges.push([ri + 1, i + 1, j + 1])
          }
          i = j + 1
        } else {
          i++
        }
      }
      const r = ws.addRow(vals)"""
s = s.replace(OLD2, NEW2, 1)

OLD3 = """    ws.views = [{ state: 'frozen', ySplit: 1 }]"""
assert s.count(OLD3) == 1, "anchor3"
NEW3 = """    // 記録した範囲を実際に結合する
    for (const [row, c1, c2] of merges) {
      try { ws.mergeCells(row, c1, row, c2) } catch { /* 既に結合済みなら無視 */ }
    }
    ws.views = [{ state: 'frozen', ySplit: 1 }]"""
s = s.replace(OLD3, NEW3, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
