# -*- coding: utf-8 -*-
"""[HEARING_XLSX_V6 2026-10-29] 連続していない重複も畳む。

V5で「連続する同一文字列」は結合できたが、カードキー(17行)などで
重複が残った。原因は結合範囲の間に空セルが挟まるケース:
    A="設問"  B=""  C="設問"  D="設問"
これは元が A1:D1 の結合で、CSV出力時に一部が空になったもの。

対策: 行内で同じ文字列が複数回出たら、最初の1つだけ残して残りを空にし、
      最初の出現位置から最後の出現位置までを結合する。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\hearing-xlsx\route.ts"
bak = P + ".bak_v6_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """      // --- 雛形の結合を復元する ---
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
      }"""
assert s.count(OLD) == 1, "anchor"

NEW = """      // --- 雛形の結合を復元する ---
      //   [HEARING_XLSX_V6] CSV化で失われた結合は「同じ文字列が複数セルに入る」形で残る。
      //   間に空セルが挟まるケース(A=設問 B='' C=設問 D=設問)もあるため、
      //   連続判定ではなく『同一文字列の最初〜最後の出現位置』を結合範囲とする。
      {
        const seen = new Map<string, number[]>()
        vals.forEach((v, idx) => {
          if (!v || v === '□' || v === '✔') return
          if (!seen.has(v)) seen.set(v, [])
          seen.get(v)!.push(idx)
        })
        for (const [v, idxs] of seen) {
          if (idxs.length < 2) continue
          const first = idxs[0]
          const last = idxs[idxs.length - 1]
          // 範囲内に別の文字列が無い場合だけ結合する（設問が消えるのを防ぐ）
          let safe = true
          for (let k = first; k <= last; k++) {
            const x = vals[k]
            if (x && x !== v) { safe = false; break }
          }
          if (!safe) {
            // 安全でない場合は重複だけ消す（最初以外を空に）
            for (let k = 1; k < idxs.length; k++) vals[idxs[k]] = ''
            continue
          }
          for (let k = first + 1; k <= last; k++) vals[k] = ''
          merges.push([ri + 1, first + 1, last + 1])
        }
      }"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
