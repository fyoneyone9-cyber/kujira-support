# -*- coding: utf-8 -*-
"""[APPLICATION_PARSE_V7 2026-10-29] contact が空になる問題を確実に直す。

デバッグで「石川　泰裕」は読めていることを確認済み。
取れない原因を推測で潰すのをやめ、**ブロック抽出に依存しない方式**にする。

新方式: 行28〜34（担当者ブロック）を label で特定し、
  7列目の値だけを順に拾う。TEL/メールアドレスのラベル行はスキップ。
  先頭2件が カナ / 漢字。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\parse-application\route.ts"
shutil.copy2(P, P + ".bak_v7_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

OLD = """  // [V4] ④担当者氏名ブロックは「カナ → 漢字 → TEL → メール」の順に並ぶ。
  //   電話番号やメールを除いた先頭2件が カナ / 漢字。
  const contactVals = blockValues(/担当者氏名/)
    .filter(v => !/@/.test(v) && !/^[\\d\\-+() ]+$/.test(v))
  const isKana = (v: string) => /^[ァ-ヶー\\s　]+$/.test(v)
  const contact = contactVals.find(v => !isKana(v)) || ''
  const contactKana = contactVals.find(isKana) || ''"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)

NEW = """  // [V7] 担当者ブロックは 7列目に「カナ → 漢字 → TEL → メール」の順で入る。
  //   ブロック抽出の条件分岐で取りこぼしていたので、7列目を直接走査する。
  const contactSeq: string[] = []
  {
    const seen = new Set<string>()
    for (const ri of blockRows(/担当者氏名/)) {
      const v = (grid[ri][7] || '').trim()
      if (!v || seen.has(v)) continue
      seen.add(v)
      if (/^(TEL|FAX|メールアドレス|〒)$/.test(v)) continue
      if (/@/.test(v)) continue
      if (/^[\\d\\-+()\\s]+$/.test(v)) continue
      contactSeq.push(v)
    }
  }
  const isKana = (v: string) => /^[ァ-ヶー\\s　]+$/.test(v)
  const contact = contactSeq.find(v => !isKana(v)) || contactSeq[0] || ''
  const contactKana = contactSeq.find(isKana) || ''"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
