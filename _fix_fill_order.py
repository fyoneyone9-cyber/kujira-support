# -*- coding: utf-8 -*-
"""[HEARING_XLSX_V9 2026-10-29] 自動入力が結合に飲み込まれる問題を修正。

原因: 処理順が
        (1) fill で ANS列に値を書く
        (2) 結合判定（テキストの連続区間を結合）
      となっており、(1)で書いた値が (2) の「次のテキスト」として扱われ、
      B列の設問が「ANS列の手前まで」で止まるのは正しいが、
      書いた値自体が結合の対象になって消えていた。

対策: 結合判定を先に済ませ、**そのあとに** fill の値を入れる。
      これで結合範囲に影響を与えずに回答欄へ書ける。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\hearing-xlsx\route.ts"
bak = P + ".bak_v9_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# fill ブロックを切り出す
i = s.index("      // [HEARING_AUTOFILL_V1] この行の項目名が fill のキーと一致したら回答欄に値を入れる")
j = s.index("      const r = ws.addRow(vals)")
fill_block = s[i:j]
s = s[:i] + s[j:]   # いったん削除

# 結合ブロックの直後に移動する
k = s.index("      const r = ws.addRow(vals)")
NEW = """      // [HEARING_XLSX_V9 2026-10-29] fill は結合判定の『後』に行う。
      //   先に書くと、その値が「次のテキスト」として結合範囲の判定に影響し、
      //   書いた値自体が結合に飲み込まれて消えていた。
      {
        const label = vals.find(v => v && v !== '□' && v !== '✔') || ''
        if (label) {
          const key = Object.keys(fill).find(k2 => label.includes(k2))
          if (key && fill[key]) {
            let target = vals.findIndex(v => v === '□')
            if (target < 0) target = ANS - 1
            while (vals.length <= target) vals.push('')
            vals[target] = fill[key]
          }
        }
      }

"""
s = s[:k] + NEW + s[k:]
io.open(P, "w", encoding="utf-8").write(s)
print("moved fill after merge")
