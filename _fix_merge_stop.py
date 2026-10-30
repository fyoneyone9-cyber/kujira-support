# -*- coding: utf-8 -*-
"""[HEARING_XLSX_V10 2026-10-29] 結合が回答欄を飲み込む問題を修正。

実測: 必須確認②で B〜H が結合され、ご回答欄は I 列。
      しかし fill で I 列(ANS=9)に書いた値が表示されない。
      → 結合範囲 B:H は正しいが、`merges` 配列を作るときに
        ANS より右の列まで含むケースがあり、I 列が従属セルになっていた。

対策: 結合の右端を必ず `ANS - 2`（回答欄の1つ手前）で打ち切る。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\hearing-xlsx\route.ts"
bak = P + ".bak_v10_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """          let end = (next !== undefined ? next - 1 : ANS - 2)
          if (cur >= ANS - 1) end = cur                // L列以降は結合しない
          if (end > cur) merges.push([ri + 1, cur + 1, end + 1])"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)
NEW = """          let end = (next !== undefined ? next - 1 : ANS - 2)
          // [HEARING_XLSX_V10] 結合は必ず回答欄の手前で止める。
          //   飲み込むと自動入力した値が従属セルになって消える。
          if (end > ANS - 2) end = ANS - 2
          if (cur >= ANS - 1) end = cur                // 回答欄以降は結合しない
          if (end > cur) merges.push([ri + 1, cur + 1, end + 1])"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
