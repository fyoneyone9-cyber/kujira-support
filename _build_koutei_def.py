# -*- coding: utf-8 -*-
"""[KOUTEI_DEF_V1 2026-10-29] 工程管理表の雛形を定義ファイル化する。

構造:
  1-2行目 = ヘッダ（会社名/物件名/稼働予定日 等）
  3行目   = 列見出し（No/品目/区分/作業名/...）
  4行目〜 = 工程データ。C列の区分で機材が分かる。

区分一覧(17種):
  01.共通 02.補助金 03.チェックインシステム 04.PMS 05.カードキー
  06.スマートロック 07.キーボックス 08.KIOSK 09.卓上KIOSK
  10.ルームタブレット 11.Surface 12.タブレット 13.P400
  14.PayCube 15.PayPay 16.スマホカード決済 17.パスポートリーダー
"""
import io, csv, glob, os, json

p = [x for x in glob.glob(r"C:\Users\fyone\Downloads\*.csv")
     if "\u5de5\u7a0b\u7ba1\u7406" in os.path.basename(x)][0]
rows = list(csv.reader(io.open(p, encoding="utf-8-sig")))

# 行末の空セルだけ落とす（列位置は保つ）
clean = []
for r in rows:
    line = [c.strip() for c in r]
    while line and line[-1] == "":
        line.pop()
    clean.append(line)

OUT = r"C:\GensparkClaw\kujira-support\src\lib\kouteiDef.ts"
f = io.open(OUT, "w", encoding="utf-8")
f.write("// [KOUTEI_DEF_V1 2026-10-29] 自動生成 (_build_koutei_def.py)\n")
f.write("// 工程管理表の原本。C列(index 2)の『区分』で機材ごとの行を判別する。\n")
f.write("// ⚠ 手で編集しないこと。原本が変わったら _build_koutei_def.py を再実行する。\n")
f.write("export const KOUTEI_ROWS: string[][] = ")
f.write(json.dumps(clean, ensure_ascii=False, indent=0))
f.write("\n\n")
f.write("""// 区分 -> この機材がある場合だけ残す
export const KOUTEI_CATEGORY_KEYS: Record<string, string> = {
 '01.共通': 'always',
 '02.補助金': 'hojokin',
 '03.チェックインシステム': 'always',
 '04.PMS': 'pms',
 '05.カードキー': 'cardkey',
 '06.スマートロック': 'smartlock',
 '07.キーボックス': 'keybox',
 '08.KIOSK': 'kiosk',
 '09.卓上KIOSK': 'kiosk_desk',
 '10.ルームタブレット': 'roomtablet',
 '11.Surface': 'surface',
 '12.タブレット': 'tablet',
 '13.P400': 'p400',
 '14.PayCube': 'paycube',
 '15.PayPay': 'paypay',
 '16.スマホカード決済': 'sumaho',
 '17.パスポートリーダー': 'passport',
}
""")
f.close()
print("rows:", len(clean))
print("wrote", OUT)
