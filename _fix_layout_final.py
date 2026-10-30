# -*- coding: utf-8 -*-
"""[HEARING_XLSX_V7 2026-10-29] 見た目を雛形に合わせる（本命修正）。

判明した事実:
  ・CSVには結合情報が無く、値は1セルにしか入っていない
      ["1. 物件で利用する『鍵』について", "", ..., "いずれか１つを"]
        A列のみ                                   L列
  ・雛形は A:K を結合して広く見せているが、生成側は A列(幅4)に長文を入れていた
    → 文字が潰れて「全然別物」に見えていた

対策:
  ・テキストが入っているセルから、次にテキストがあるセルの手前までを結合する
    (A列の文 -> K列まで結合 / B列の文 -> K列まで結合 / L列は回答欄で独立)
  ・列幅はA〜Kを合計で読める幅に配分し、L列(回答欄)を広く取る
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\hearing-xlsx\route.ts"
bak = P + ".bak_v7_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# --- 列幅 ---
OLD_W = """    const ANS = 12                                   // L列 = 回答欄
    const maxCols = Math.max(...def.map(r => r.length), ANS)
    ws.columns = Array.from({ length: maxCols }, (_, i) => {
      if (i === 0) return { width: 4 }
      if (i === 1) return { width: 8 }
      if (i === 2) return { width: 4 }
      if (i === 3) return { width: 8 }
      if (i === ANS - 1) return { width: 26 }        // ご回答欄
      if (i >= ANS) return { width: 44 }             // 備考など
      return { width: 8 }
    })"""
assert s.count(OLD_W) == 1, "anchor width"
NEW_W = """    const ANS = 12                                   // L列 = ご回答欄
    const maxCols = Math.max(...def.map(r => r.length), ANS)
    // [HEARING_XLSX_V7] A〜K は結合して1つの文章枠として使うので、
    //   合計で読める幅になるよう配分する（A=インデント, B以降=本文）。
    ws.columns = Array.from({ length: maxCols }, (_, i) => {
      if (i === 0) return { width: 3 }               // インデント用
      if (i === 1) return { width: 10 }
      if (i === 2) return { width: 3 }
      if (i >= 3 && i <= ANS - 2) return { width: 9 }  // D〜K（結合して本文になる）
      if (i === ANS - 1) return { width: 24 }        // L ご回答欄
      return { width: 40 }                            // M以降 備考
    })"""
s = s.replace(OLD_W, NEW_W, 1)

# --- 結合ロジックを置き換え ---
i = s.index("      // --- 雛形の結合を復元する ---")
j = s.index("      const r = ws.addRow(vals)")
NEW_M = """      // --- [HEARING_XLSX_V7] テキストセルを次のテキストの手前まで結合する ---
      //   CSVには結合情報が無く値は1セルだけなので、そのままだと細い列に
      //   長文が入って潰れる。雛形と同じく横に広げて読めるようにする。
      {
        const textIdx: number[] = []
        vals.forEach((v, idx) => { if (v) textIdx.push(idx) })
        for (let n = 0; n < textIdx.length; n++) {
          const cur = textIdx[n]
          const next = textIdx[n + 1]
          const v = vals[cur]
          if (v === '□' || v === '✔') continue        // 回答欄は結合しない
          // 結合の右端: 次のテキストの手前、無ければ回答欄(L)の手前
          let end = (next !== undefined ? next - 1 : ANS - 2)
          if (cur >= ANS - 1) end = cur                // L列以降は結合しない
          if (end > cur) merges.push([ri + 1, cur + 1, end + 1])
        }
      }

"""
s = s[:i] + NEW_M + s[j:]

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
