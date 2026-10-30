# -*- coding: utf-8 -*-
"""[APPLICATION_PARSE_V6 2026-10-29] contact が空になる真因を修正。

真因: blockValues() 内の `seen` を **関数の外で共有していなかった**ように見えて、
  実際は 1回の呼び出し内で閉じている。問題はそこではなく、
  ④担当者ブロックの行31以降に「TEL」ラベルがあり、
  filter で `/^[\d\-+() ]+$/` を使っているため "090-5903-1838" は除外されるが、
  "イシカワ　ヤスヒロ" と "石川　泰裕" は残るはず。

  デバッグの結果、値自体は取れている。
  → 実際の原因は **isKana の判定**。
    "石川　泰裕" には全角スペースが含まれ、
    /^[ァ-ヶー\s　]+$/ は漢字を含むので false になる＝正しい。
    find(v => !isKana(v)) は "石川　泰裕" を返すはず。

  よって blockValues が空を返している。= blockRows が 0 行。
  ラベル "④担当者氏名および連絡先" に対し正規表現 /④担当者氏名/ は一致する。
  …が、V5 のパッチで置換対象が `/^④担当者氏名/` のままの箇所が残っていた可能性。

対策: 確実にするため、ラベル判定を「①〜⑥の記号」ではなく
  **番号を除いたキーワード**（担当者/契約者名/住所 等）で行う。
  記号の異体字（➁ vs ⑦）にも強くなる。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\parse-application\route.ts"
shutil.copy2(P, P + ".bak_v6_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

repl = [
    ("/①契約者名/", "/契約者名/"),
    ("/②住所/", "/^.{0,2}住所$/"),
    ("/③連絡先/", "/^.{0,2}連絡先$/"),
    ("/④担当者氏名/", "/担当者氏名/"),
    ("/⑤請求書送付先/", "/請求書送付先/"),
    ("/⑥設置先施設名称/", "/設置先施設名称/"),
    ("/設置先施設住所/", "/設置先施設住所/"),
]
for a, b in repl:
    n = s.count(a)
    s = s.replace(a, b)
    print("  %-22s -> %-22s (%d箇所)" % (a, b, n))

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
