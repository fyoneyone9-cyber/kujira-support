# -*- coding: utf-8 -*-
"""[APPLICATION_PARSE_V5 2026-10-29] 担当者と連絡先を正しく取る。

残課題:
 (1) contact が空
     実データ(行28-34)は 1列目が「④担当者氏名  および連絡先」で、
     ラベルに全角スペースが2つ入る。正規表現 /^④担当者氏名/ は
     replace(/\\s+/g,'') 後に当てているので "④担当者氏名および連絡先" となり一致する。
     → 一致はしている。問題は blockValues の重複除去で、
       先に ③連絡先ブロックを処理していないため…ではなく、
       「石川　泰裕」が既に seen に入っていないか確認が必要。
     実際は contactVals が [イシカワ ヤスヒロ, 石川 泰裕] になるはずだが
     isKana が全角スペースを許容していても、"石川　泰裕" は漢字なので find で取れる。
     → 原因は blockRows のラベル照合。1列目は「④担当者氏名  および連絡先」で
       改行が入っており、replace(/\\s+/g,'') で消えるが
       正規表現を /^④担当者氏名/ ではなく部分一致にする方が安全。

 (2) 担当者の TEL/メール を優先したい
     ③連絡先 = 会社代表、④担当者 = 担当者個人。
     ヒアリングシートには担当者の連絡先を入れるべき。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\parse-application\route.ts"
shutil.copy2(P, P + ".bak_v5_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

# ラベル照合を部分一致に（先頭一致だと記号のゆらぎで外れる）
OLD = """  const blockRows = (labelRe: RegExp) =>
    rowNums.filter(ri => labelRe.test((grid[ri][1] || '').replace(/\\s+/g, '')))"""
assert s.count(OLD) == 1, "anchor1"
NEW = """  // [V5] ラベルは「④担当者氏名  および連絡先」のように空白/改行が入るので
  //   空白を除いてから部分一致で判定する。
  const blockRows = (labelRe: RegExp) =>
    rowNums.filter(ri => labelRe.test((grid[ri][1] || '').replace(/[\\s　]+/g, '')))"""
s = s.replace(OLD, NEW, 1)

# 各ラベルを部分一致に変更
for a, b in [
    ("/^①契約者名?$/", "/①契約者名/"),
    ("/^②住所$/", "/②住所/"),
    ("/^③連絡先$/", "/③連絡先/"),
    ("/^④担当者氏名/", "/④担当者氏名/"),
    ("/^⑤請求書送付先/", "/⑤請求書送付先/"),
    ("/^⑥設置先施設名称/", "/⑥設置先施設名称/"),
]:
    s = s.replace(a, b)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
