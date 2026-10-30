# -*- coding: utf-8 -*-
"""[HEARING_XLSX_V4] 1行にB列とD列の両方へテキストがある場合、
結合でD列(本来の設問)が消えるバグを修正する。

実例(雛形 必須確認① 16行目):
  B列 = 「※『精算機能』を利用される場合は、右の質問にもご回答ください」(注記)
  D列 = 「決済手段として『現金支払い』を導入されますか？」(設問) ← これが消えていた

対策: 最初のテキスト列から結合するのではなく、
      「テキストが入っている最後の列」を設問本体とみなし、そこから回答欄手前まで結合する。
      それより左のセルは注記としてそのまま残す。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\hearing-xlsx\route.ts"
bak = P + ".bak_mergebug_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """      // テキストが入っている最初の列を調べ、A〜K列を結合して読めるようにする
      let firstText = -1
      for (let c = 0; c < Math.min(vals.length, ANS); c++) {
        if (vals[c] && vals[c] !== '□') { firstText = c; break }
      }
      if (firstText >= 0) {"""
assert s.count(OLD) == 1, "anchor"

NEW = """      // [HEARING_XLSX_V4] 1行にB列とD列の両方へテキストがある場合がある。
      //   例) B列=「※右の質問にもご回答ください」(注記) / D列=「現金支払いを導入しますか？」(設問)
      //   最初のテキスト列から結合すると D列の設問が消えるため、
      //   『最後のテキスト列』を設問本体とみなして、そこから回答欄手前まで結合する。
      const textCols: number[] = []
      for (let c = 0; c < Math.min(vals.length, ANS); c++) {
        if (vals[c] && vals[c] !== '□') textCols.push(c)
      }
      const firstText = textCols.length ? textCols[textCols.length - 1] : -1
      // 左側に注記がある場合は折り返して表示できるよう幅を確保
      if (textCols.length > 1) {
        const noteCol = textCols[0]
        const nc = r.getCell(noteCol + 1)
        nc.alignment = { wrapText: true, vertical: 'middle' }
        nc.font = { size: 9, color: { argb: 'FF777777' } }
        try { ws.mergeCells(r.number, noteCol + 1, r.number, firstText) } catch { /* noop */ }
      }
      if (firstText >= 0) {"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
